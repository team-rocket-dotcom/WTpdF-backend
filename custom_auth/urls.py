from django.urls import path
from .views import LoginView, RegisterView, GoogleOAuthView

app_name = 'custom_auth'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('google', GoogleOAuthView.as_view(), name='google-oauth')
]