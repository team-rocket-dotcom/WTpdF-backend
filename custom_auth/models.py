from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.db import models
from decouple import config
import uuid

AUTH_PROVIDERS = (
    ('email', 'Email'),
    ('google', 'Google')
)

class CustomUserManager(BaseUserManager):

    def create_user(self, email, auth_provider= 'email', password= None, *args, **kwargs):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        if auth_provider == 'email':
            kwargs['social_id'] = email
            user = self.model(email=email, auth_provider=auth_provider, *args, **kwargs)

            if not password:
                raise ValueError('Password is required for email sign-in.')
            
            user.set_password(password)

        elif auth_provider=='google':
            user= self.model(email=email, auth_provider=auth_provider, *args, **kwargs)
            user.set_unusable_password()

        user.save(using= self._db)
        return user
    

class CustomUser(AbstractBaseUser,  PermissionsMixin):

    id = models.CharField(max_length=10, unique=True, primary_key=True)
    social_id= models.CharField(max_length=230, unique=True, default='')

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    picture = models.URLField(default=config('USER_PFP'))

    auth_provider = models.CharField(
        max_length = 20,
        choices = AUTH_PROVIDERS,
        default = 'email'
    )

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f'{uuid.uuid4().hex[:8].lower()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.auth_provider})"