from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError
            'User with the same email is already exists'
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password != password2:
            raise serializers.ValidationError('Password does not match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User was not found')
        return email

    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(
                username=email,
                password=password,
                request=request
            )

            if not user:
                raise serializers.ValidationError('Not valid email or password')
        else:
            raise serializers.ValidationError('Email and password must be filled')

        data['user'] = user
        return data
