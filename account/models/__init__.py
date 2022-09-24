"""This will work as a __init__ method in a default models.py file"""

from django.conf import settings
from django.contrib.auth.models import Group
# from rest_framework.authtoken.models import Token as DefaultTokenModel
# from eventapiapp.utils import import_callable

from .users import MyUserManager, User
from .blog import Blog


#TokenModel = import_callable(getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel))
