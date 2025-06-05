from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.db import models

AUTH_PROVIDERS = (
    ('email', 'Email'),
    ('google', 'Google')
)

class CustomUserManager(BaseUserManager, PermissionsMixin):

    def create_user(self, email, auth_provider= 'email', password= None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.create_user(email=email, auth_provider=auth_provider, **extra_fields)

        if auth_provider == 'email':
            if not password:
                raise ValueError('Password is required for email sign-in.')
            
            user.set_password(password)

        else:
            user.set_unusable_password()

        user.save(using= self._db)
        return user
    

class CustomUser(AbstractBaseUser):

    id = models.CharField(unique=True)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    picture = models.URLField()

    auth_provider = models.CharField(
        max_length = 20,
        choices = AUTH_PROVIDERS,
        default = 'email'
    )

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.auth_provider})"