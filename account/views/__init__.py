"""
You can import your all individual views here,

These imported views can be directly accessible throughout the Application.

This __init__ file works same as a default __init__ method in any class OR function.
"""

from .user import UserRegistrationView, UserLoginView, UserProfileView, activate
from .blog import BlogCreateView, GetAllBlogs
