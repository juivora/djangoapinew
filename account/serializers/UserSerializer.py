from dataclasses import dataclass, fields
from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


from account.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(
    #     min_length=4, max_length=100, write_only=True)
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    # last_login =

    class Meta:
        model = User
        fields = ['email', 'name', 'tc', 'password', 'password2']
        # write_only_fields = ['password2']
        read_only_fields = ['last_login']
        extra_kwargs = {
            'password': {'write_only': True},
            # 'last_login': {'read_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        newpassword = data.get('password2')

        if password != newpassword:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        user = authenticate(**data)
        if user is not None:
            if user.is_verified:
                # added user model to OrderedDict that serializer is validating
                data['user'] = user
                return data  # and in sunny day scenario, return this dict, as everything is fine
            else:
                raise serializers.ValidationError("Account is not activated")
        raise exceptions.AuthenticationFailed()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']
