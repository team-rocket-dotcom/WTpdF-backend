from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .services import gooogle_authentication
# Create your views here.

class GoogleLoginView(APIView):
    http_method_names = ['post']

    def post(self, request):

        id_token = request.data.get('id_token')

        if not id_token:
            raise ValidationError({"id_token": "This field is required."})

        try:    
            user = gooogle_authentication(id_token)
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user":
                {
                    "id": user.id,
                    "email": user.email,
                    "name": f"{user.first_name} {user.last_name}"
                }
            })
        except ValueError:
            return Response({"error": "Invalid Google ID token"}, status= status.HTTP400)