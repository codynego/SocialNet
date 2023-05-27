from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.http import urlsafe_base64_decode

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserRegistration(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=60, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def create(self, attrs):
        attrs.pop('confirm_password')
        user = User.objects.create_user(**attrs)
        return user
    
    def validate(self, attrs):
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError('password doesnt match')
        return attrs
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

class ResendVerificationEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid or expired.', 401)
            user.set_password(password)
            user.save()

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid has expired.', 401)
        return super().validate(attrs)
    

class LogoutSerializer(serializers.Serializer):
    refresh_token =  serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise ValidationError({'incorrect_token': 'The token is either invalid or expired'})