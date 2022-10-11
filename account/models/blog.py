"""This is a model module to store Blog data in to the database"""

from distutils.command.upload import upload
from pyexpat import model
from django.conf import settings
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from account.models.users import User
from s3direct.fields import S3DirectField


# ----------------------------------------------------------------------
# Blog  Model
# ----------------------------------------------------------------------


class Blog(models.Model):
    """This model stores the data into Blog table in db"""

    title = CharField(_("title"), db_index=True,
                      max_length=255)
    description = models.TextField(default='')
    # image = CharField(_("image"), db_index=True, blank=True, cmax_length=255, required=True)
    # image = S3DirectField(dest='primary_destination', blank=True)
    image = models.FileField(upload_to='media/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_user')
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, )
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, )

    class Meta:
        """Provide some extra information here"""

        verbose_name = "blog"
        verbose_name_plural = "blogs"

    # def get_absolute_url(self):
    #     """Redirect to the absolute url on successful action with specified data"""

    #     return reverse("core:event-list", kwargs={"name": self.name})

    # def __str__(self):
    #     return "{0}".format(self.name)
