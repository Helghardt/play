import os
import uuid
import time

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now

from administration.models import User
import requests
from django.conf import settings


def get_unique_filename(filename):
    name, ext = os.path.splitext(filename)
    return "{}_{}{}".format(uuid.uuid4().hex, str(int(time.time())), ext)


def get_image_path(instance, filename):
    return os.path.join('users', str(instance.user.id), 'images', get_unique_filename(filename))


class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.

    By default, sets editable=False, default=datetime.now.

    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)


class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.

    By default, sets editable=False and default=datetime.now.

    """

    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value


class TimeStampedModel(models.Model):
    created_at = AutoCreatedField()
    modified_at = AutoLastModifiedField

    class Meta:
        abstract = True


class Photo(TimeStampedModel):
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    data = JSONField(default={}, null=True, blank=True)
    is_profile = models.BooleanField(default=False)

    def __str__(self):
        return 'Photo {}'.format(self.pk)

    def save(self, *args, **kwargs):
        super(Photo, self).save()
        self.face_detect()

    def face_detect(self):

        url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=true&returnFaceAttributes=age,gender,headPose,smile,facialHair,glasses'
        data = open(getattr(settings, 'PROJECT_DIR') + '/var/www/' + self.image.url, 'rb').read()
        res = requests.post(
            url=url,
            data=data,
            headers={
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': getattr(settings, 'MICROSOFT_FACE_API_KEY')
            }
        )

        self.data = res.json()

    def find_similar(self):
        self.save()

    def add_face_to_list(self):
        self.save()
