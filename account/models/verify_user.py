"""This is a model module to store Blog data in to the database"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models.users import User


# ----------------------------------------------------------------------
# Verify User  Model
# ----------------------------------------------------------------------


class VerifyUser(models.Model):
    """This model stores the data into Blog table in db"""

   
    token = models.TextField(default='')     
    user = models.ForeignKey("user", db_index=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, )

    class Meta:
        """Provide some extra information here"""

        verbose_name = "verifyuser"
        verbose_name_plural = "verifyusers"