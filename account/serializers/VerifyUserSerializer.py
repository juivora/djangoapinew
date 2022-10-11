from rest_framework import serializers
# from django.contrib.auth import authenticate
from account.models import VerifyUser


class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyUser
        fields = ['id', 'token', 'user']
