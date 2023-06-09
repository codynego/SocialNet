from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import UserSerializer, UserRegistration, LoginSerializer, RequestPasswordResetEmailSerializer, SetNewPasswordSerializer, EmailVerificationSerializer, ResendVerificationEmailSerializer, LogoutSerializer
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from userprofile.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.urls import reverse
from .utils import Mail
from django.conf import settings
from django.core.mail import send_mail
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
import traceback
from django.views.decorators.csrf import csrf_exempt


class RegistrationView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistration
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate and send the verification email
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request)
        relative_link = reverse('verify-email')
        verification_link = 'http://' + current_site.domain + relative_link + "?token=" + str(token)

        email_subject = 'Email Verification'
        email_body = f"Hi {user.username},\n\nPlease use the link below to verify your email:\n{verification_link}\n\nIf you were not expecting any account verification email, please ignore this message."

        data = {'email_body': email_body,'to_email': user.email,
         'email_subject': email_subject}

        Mail.send_email(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmailVerificationView(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_active = True
                user.save()
            return Response({'Email Successfully verified'}, status = status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status= status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            
    

class ResendVerificationEmailView(APIView):
    serializer_class = ResendVerificationEmailSerializer

    def post(self, request):
        input_data = request.data
        email = input_data['email']

        try:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email__exact=email)
                token = RefreshToken.for_user(user).access_token
                current_site_domain = get_current_site(request).domain
                relative_link = reverse('verify-email')
                verification_link = 'https://' + current_site_domain + relative_link + "?token=" + str(token)

                message = ". Use the link below to verify your email.\n If you were not expecting any account verification email, please ignore this.\n"
                email_body = "Hi " + email + message + verification_link
                data = {
                    'email_body': email_body,
                    'to_email': email,
                    'email_subject': 'Demo Email Verification'
                }

                Mail.send_email(data)
                return Response({'message': 'Verification email sent. Check your inbox.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'The email address does not match any user account.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            traceback.print_exc()
            return Response({'message': 'Something went wrong.'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        Email = request.data['email']
        
        if User.objects.filter(email=Email).exists():
            user = User.objects.get(email=Email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink 
            
            email_body = "Hello! \n Use the link below to reset your password \n" + absurl
            data = {'email_body': email_body,'to_email': user.email,
                    'email_subject':'Reset your password'}
            
            Mail.send_email(data)
            
        return Response({'Success': 'Password reset email sent'}, status=status.HTTP_200_OK)
    
class PasswordResetTokenValidationView(generics.GenericAPIView):
    
    def get(self, request, uidb64, token):
        
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'Error': 'Password reset link is expired! Please request for a new one!'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'Success':True, 'Message':'Valid Credentials','uidb64':uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as exc:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'Error': 'Token is not valid! Please request for a new one!'}, status=status.HTTP_401_UNAUTHORIZED)
            

class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message':'Password changed successfully'}, status= status.HTTP_200_OK)



class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': True, 'message':'Logged out successfully'},status=status.HTTP_200_OK)