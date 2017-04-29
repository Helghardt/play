import datetime
import os
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.timezone import utc
from everything.utils.common import get_unique_filename


# Create your models here.
from rest_framework.fields import JSONField


class Text(models.Model):
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.info


class Rating(models.Model):
    rating = models.PositiveIntegerField()

    def __int__(self):
        return self.rating


def get_image_path(instance, filename):
    return os.path.join('images', get_unique_filename(filename))


class Image(models.Model):
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    data = JSONField(default={})
    is_profile = models.BooleanField(default=False)

    def __str__(self):
        return 'Image {}'.format(self.pk)

    def save(self, *args, **kwargs):
        super(Image, self).save()


class InputType(models.Model):
    slug = models.CharField(max_length=50, blank=True, null=True) # e.g. rating, text, geo
    description = models.CharField(max_length=250, blank=True, null=True) # Rating, Text, Geo Location
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    user = models.ForeignKey('administration.User', blank=True, null=True)
    slug = models.CharField(max_length=100, blank=True, null=True) #
    description = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    custom = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.slug


class RecipeInput(models.Model):
    recipe = models.ForeignKey(Recipe)
    input_type = models.ForeignKey(InputType)

    def __str__(self):
        return self.recipe.slug


class Log(models.Model):
    user = models.ForeignKey('administration.User')
    recipe = models.ForeignKey(Recipe, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:  # On create
            self.created = datetime.datetime.now(tz=utc)

        self.updated = datetime.datetime.now(tz=utc)
        return super(Log, self).save(*args, **kwargs)

    def build(self, rating):

        try:
            recipe_input = RecipeInput.objects.filter(recipe=self.recipe)
            for i in recipe_input:
                if i.input_type.slug == 'rating':
                    obj = Rating.objects.create(rating=rating)
                    content_type = ContentType.objects.get_for_model(obj)
                    LogInput.objects.create(log=self,
                                            recipe_input=i,
                                            content_type=content_type,
                                            object_id=obj.id)
        except:
            return _("Sorry, could not eat that.")


class LogInput(models.Model):
    log = models.ForeignKey(Log)
    recipe_input = models.ForeignKey(RecipeInput)
    # Relates to the actual input model, Text, Image, etc. and it's entry by id.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.log.title