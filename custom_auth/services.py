from .models import CustomUser
from .serializers import UserSerializer
from google.oauth2 import id_token
from google.auth.transport import requests as google_req
from decouple import config

def email_authentication(data):
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return None, False, {"error": "Email and password are required."}

    existing_user = CustomUser.objects.filter(email=email).first()
    if existing_user:
        if not existing_user.check_password(password):
            return None, False, {"error":"Invalid Password"}
        return existing_user, False, None
    
    data['auth_provider'] = 'email'

    serializer = UserSerializer(data=data)
    if not serializer.is_valid():
        return None, False,serializer.errors

    user = serializer.save()

    return user, True,None

def google_authentication(id_token_str):
    try:
        user_info = id_token.verify_oauth2_token(
            id_token_str,
            google_req.Request(),
            audience = config('GOOGLE_CLIENT_ID')
        )

        if user_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None, False, {"error": "Invalid issuer"}

        email = user_info.get('email')
        existing_user = CustomUser.objects.filter(email=email)

        if existing_user:
            return existing_user, False, None
        
        user_data = {
            'email': email,
            'first_name': user_info.get('given_name'),
            'last_name': user_info.get('family_name'),
            'picture': user_info.get('picture'),
            'auth_provider': 'google'
        }

        serializer = UserSerializer(data= user_data)
        if not serializer.is_valid():
            return None, False, serializer.errors
        
        user = serializer.save()
        return user, True, None

    except Exception as e:
        return None, False,{"error": str(e)}

def authenticate_user(data):

    if data.get('email'):
        return email_authentication(data)

    elif data.get('id_token'):
        id_token = data.get('id_token')
        return google_authentication(id_token)
    
    return None, False, {"error": "Missing email or id_token in request."}