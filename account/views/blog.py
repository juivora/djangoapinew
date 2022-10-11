import os
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from datetime import datetime
from boto3.session import Session

from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view
from rest_framework import viewsets, parsers, generics, status
# from rest_framework.parsers import MultiPartParser


# from account.renderers import UserRenderer
from account.models import Blog
# from account import serializers
from account.serializers import BlogSerializer, BlogUpdateSerializer


class GetAllBlogs(APIView):
    serializer_class = BlogSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get(self, request, format=None):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response({"message": "Got Successful", "success": True, "data": serializer.data}, status=status.HTTP_200_OK)


class BlogCreateView(APIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        id = pk
        user = request.user
       
        if id is not None:
            # get blogs by specific id for authenticated user only
            blog = Blog.objects.filter(id=id, user=user)
            serializer = BlogSerializer(blog, many=True)

            return Response({"message": "Got Successful", "data": serializer.data, "success": True}, status=status.HTTP_200_OK)

        # get blogs of autenticated user
        blogs = Blog.objects.filter(user=user)
        serializer = BlogSerializer(blogs, many=True)
        return Response({"message": "Got Successful", "data": serializer.data, "success": True}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            file_extension = os.path.splitext(str(request.FILES['image']))[1]
            filename = datetime.now().strftime("%d-%m-%YT%H:%M:%S") + file_extension
            session = Session(region_name=settings.AWS_S3_REGION_NAME,
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3 = session.resource('s3')
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=filename, Body=request.FILES['image'])
            serializer.save(user=request.user)
            return Response({"message": "Upload Successful", "data": serializer.data, "success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, {"success": False}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        user = request.user
        blog = Blog.objects.filter(user=user.id, id=pk).first()
      
        if blog is None:
            return Response({"success": False, "message": 'This blog owned by someone else.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BlogUpdateSerializer(blog, data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.FILES['image']:
                file_extension = os.path.splitext(
                    str(request.FILES['image']))[1]
                filename = datetime.now().strftime("%d-%m-%YT%H:%M:%S") + file_extension
                session = Session(region_name=settings.AWS_S3_REGION_NAME,
                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                s3 = session.resource('s3')
                s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                    Key=filename, Body=request.FILES['image'])
            serializer.save()
            return Response({"message": "Update Successful", "data": serializer.data, "success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, {"success": False}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None, format=None):
        user = request.user

        blog = Blog.objects.get(user=user, id=pk)

        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.FILES:
                file_extension = os.path.splitext(
                    str(request.FILES['image']))[1]
                filename = datetime.now().strftime("%d-%m-%YT%H:%M:%S") + file_extension
                session = Session(region_name=settings.AWS_S3_REGION_NAME,
                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                s3 = session.resource('s3')
                s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                    Key=filename, Body=request.FILES['image'])
            serializer.save()
            return Response({"message": "Update Successful", "data": serializer.data,  "success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, {"success": False}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        blog = Blog.objects.filter(user=request.user.id, id=pk)
        if not blog:
            return Response({"success": False, "message": 'This blog is owned by someone else or does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        blog.delete()
        return Response({"message": "Blog deleted successfully."}, status=status.HTTP_200_OK)
