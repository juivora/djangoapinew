"""
You can import your all individual serializers here,

These imported serializers can be directly accessible throughout the Application.

This __init__ file works same as a default __init__ method in any class OR function.
"""

from .UserSerializer import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .BlogSerializer import BlogSerializer, BlogUpdateSerializer
