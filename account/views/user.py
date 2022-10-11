import os
import uuid
from django.shortcuts import render
from django.http import HttpResponse
from account.serializers.VerifyUserSerializer import VerifyUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
import datetime
import json

from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers

from uuid import uuid4
# import uuid
from djangoapi import settings
from account.serializers import UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
from account.renderers import UserRenderer
from account.tasks import send_verification_mail_func
from account.models import User, VerifyUser, verify_user


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    # renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_data = serializer.data
       
            confirmation_token = str(uuid.uuid1()).replace("-", "")           
            verifyData = {'user': user.pk, 'token': confirmation_token}
            verifyUserSerializer = VerifyUserSerializer(data=verifyData)
            if (verifyUserSerializer.is_valid(raise_exception=True)):
                verifyUserSerializer.save()
                activation_link = f'http://{request.get_host()}/api/verifyuser/?user_id={user.pk}&confirmation_token={confirmation_token}'
               
                send_verification_mail_func(activation_link, user)
                # mail_subject = "Hye from celery"
                # message = "Please verify your account. " + activation_link
               
                # to_email = 'juivora1990@gmail.com'

                # send_mail(
                #     subject=mail_subject,
                #     message=message,
                #     from_email=settings.EMAIL_HOST_USER,
                #     recipient_list=[to_email],
                #     fail_silently=True,
                # )              
                return Response({"data": user_data, "success": True, "msg": 'Registration Successful', 'status': status.HTTP_201_CREATED})
        return Response(serializer.errors, {"success": False}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
       
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # user = serializers.serialize("json",serializer.validated_data)
            data = serializer.data
            user = User.objects.get(email=data['email'])
            token = get_tokens_for_user(user)
            return Response({'token': token,  "msg": 'Login Successful', "success": True, 'status': status.HTTP_200_OK})
        return Response(serializer.errors, {"success": False}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)      
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestMail(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, *args, **kwargs):
        send_verification_mail_func.delay()
        return Response('ok', status=status.HTTP_200_OK)


@api_view()
def activate(request, pk=None):

    user_id = request.query_params.get('user_id', '')
    confirmation_token = request.query_params.get('confirmation_token', '')
    user = User.objects.get(pk=user_id)

    if user is None:
        return Response('User not found', status=status.HTTP_400_BAD_REQUEST)

    verify_user = VerifyUser.objects.get(
        user=user.id, token=confirmation_token)
    if verify_user is None:
        return Response('Token is invalid.', status=status.HTTP_400_BAD_REQUEST)

    user.is_verified = True
    user.save()
    return Response('Email successfully confirmed')
