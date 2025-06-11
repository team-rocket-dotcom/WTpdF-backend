from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .services import authenticate_user
# Create your views here.


class LoginView(APIView):
    http_method_names = ['post']

    def post(self, request):
        
        data = request.data.copy()
        user, created, error = authenticate_user(data)

        if not user or error:
            return Response({"error":error}, status= status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access":str(refresh.access_token),
            "refresh": str(refresh),
            "user":
            {
                "id": user.id,
                "email": user.email,
                "name": f"{user.first_name} {user.last_name}"
            }
        })