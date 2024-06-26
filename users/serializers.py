from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password')
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, data):
        user = User(**data)
        password = data.get('password')

        try:
            validate_password(password,user)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)      
            raise exceptions.ValidationError({
                'password':'password_invalid',
                'error_message':serializer_errors['non_field_errors']
            })
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = validated_data['password'],
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','profile','first_name','last_name','email','password')








        