from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, exceptions, permissions
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken

from .serializers import UserSerializer, RegisterSerialzer,LoginSerializer, GoogleOAuthSerializer
from .tokens import get_tokens_for_user
# Create your views here.

class RegisterView(GenericAPIView):
    http_method_names = ['post']
    serializer_class = RegisterSerialzer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.save()

        refresh_token, access_token = get_tokens_for_user(user=user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': refresh_token,
            'access': access_token,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    
class LoginView(GenericAPIView):
    serializer_class= LoginSerializer
    permission_classes =[permissions.AllowAny]
    http_method_names = ['post']

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(request,**serializer.validated_data)
        
        if not user:
            raise exceptions.AuthenticationFailed("user does not exist.")
        
        refresh_token, access_token =get_tokens_for_user(user=user)

        return Response({
            "access":access_token,
            "refresh": refresh_token,
            "user":UserSerializer(user).data,
            'message': "User logged in successfully."
        },status=status.HTTP_200_OK)

class GoogleOAuthView(GenericAPIView):
    serializer_class= GoogleOAuthSerializer
    permission_classes=[permissions.AllowAny]
    http_method_names=['post']

    def post(self, request):
        serializer= self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request=request, **serializer.validated_data)

        if not user:
            raise exceptions.AuthenticationFailed

        refresh_token, access_token = get_tokens_for_user(user=user)

        return Response({
            'refresh': refresh_token,
            'access': access_token,
            'user': UserSerializer(user).data,
            'message':'Logged in with Google successfully.',
        }, status=status.HTTP_200_OK)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer= self.get_serializer(request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except InvalidToken as e:
            return Response({
                'code':'token_not_valid',
                'message':str(e)
            },status=status.HTTP_401_UNAUTHORIZED)
        
        validated_data= serializer.validated_data

        refresh_token_object = serializer.token_class(request.data['refresh'])
        user = refresh_token_object.user

        return Response({
            **validated_data,
            "user":UserSerializer(user).data
        },status=status.HTTP_200_OK)