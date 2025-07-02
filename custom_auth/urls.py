from django.urls import path
from .views import LoginView, RegisterView, GoogleOAuthView,CustomTokenRefreshView

app_name = 'custom_auth'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('google', GoogleOAuthView.as_view(), name='google-oauth'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token-refresh')
]