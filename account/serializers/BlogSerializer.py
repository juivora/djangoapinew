from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate


from account.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'image', 'user_id']

    # def update(self, person, validated_data):
