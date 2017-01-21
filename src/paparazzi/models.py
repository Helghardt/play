import os
import uuid
import time

from django.db import models
from django.contrib.postgres.fields import JSONField

from administration.models import User


def get_unique_filename(filename):
    name, ext = os.path.splitext(filename)
    return "{}_{}{}".format(uuid.uuid4().hex, str(int(time.time())), ext)


def get_image_path(instance, filename):
    return os.path.join('users', str(instance.user.id), 'images', get_unique_filename(filename))


class CreatedAt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Photo(CreatedAt):
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    data = JSONField(default={}, null=True, blank=True)
    is_profile = models.BooleanField(default=False)
