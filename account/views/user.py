import os
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view


from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator

from account.serializers import UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
from account.renderers import UserRenderer
from account.tasks import send_verification_mail_func
from account.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # send_verification_mail_func.delay(user)
            confirmation_token = default_token_generator.make_token(user)
            # token = get_tokens_for_user(user)
            activate_link_url = os.environ.get('BASE_URL')
            activation_link = f'{activate_link_url}?user_id={user.id}&confirmation_token={confirmation_token}'

            send_verification_mail_func.delay(activation_link, user)
            return Response({"msg": 'Registration Successful', 'status': status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token = get_tokens_for_user(user)
            return Response({'token': token, "msg": 'Login Successful', "success": True, 'status': status.HTTP_200_OK})
        return Response(serializer.errors, {"success": False}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        # if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestMail(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, *args, **kwargs):
        send_verification_mail_func.delay()
        return Response('ok', status=status.HTTP_200_OK)


@api_view()
def activate(request, pk=None):
    user_id = request.query_params.get('user_id', '')
    # print('user_id', user_id)
    confirmation_token = request.query_params.get('confirmation_token', '')
    try:
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError):
        user = None
    if user is None:
        return Response('User not found', status=status.HTTP_400_BAD_REQUEST)
    if not default_token_generator.check_token(user, confirmation_token):
        return Response('Token is invalid or expired. Please request another confirmation email by signing in.', status=status.HTTP_400_BAD_REQUEST)
    user.is_verified = True
    user.save()
    return Response('Email successfully confirmed')
