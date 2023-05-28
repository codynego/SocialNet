from django.urls import path
from .views import Timeline

urlpatterns = [
    path('timeline/', Timeline.as_view(), name='timeline'),
]