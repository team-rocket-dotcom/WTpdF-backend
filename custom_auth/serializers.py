from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id','password', 'email', 'first_name', 'last_name', 'picture']
        extra_kwargs={
            'id': {'read_only':True},
            'picture': {'required':False}
        }

    def validate(self, data):
        auth_provider = data.get('auth_provider', 'email')

        if auth_provider == 'email':

            if not data.get('password'):
                raise serializers.ValidationError({"password":"This field is required."})
            elif not data.get('first_name'):
                raise serializers.ValidationError({"first_name":"This field is required."})
            elif not data.get('last_name'):
                raise serializers.ValidationError({"last_name":"This field is required."})
        
        return data
    
    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email":"User with this email already exists."})
        return email
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        auth_provider = validated_data.get('auth_provider')

        user = CustomUser(**validated_data)

        if auth_provider == 'email' and password:
            user.set_password(password)

        else:
            user.set_unusable_password()

        user.save()
        return user
