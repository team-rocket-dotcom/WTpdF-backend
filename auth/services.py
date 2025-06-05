from .models import CustomUser
from google.oauth2 import id_token
from google.auth.transport import requests as google_req
from decouple import config

def gooogle_authentication(id_token_str):

    user_info = id_token.verify_oauth2_token(
        id_token_str,
        google_req.Request(),
        audience = config('GOOGLE_CLIENT_ID')
    )

    if user_info['iss'] in ['accounts.google.com', 'https://accounts.google.com']:

        sub = user_info['sub']
        email = user_info['email']
        first_name = user_info['given_name']
        last_name = user_info['family_name']
        picture = user_info['picture']

        user = CustomUser.objects.get_or_create(
            unique_id = sub,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name' : last_name,
                'picture' : picture,
                'auth_provider' : 'google'
            }
        )

        return user
    
    return None