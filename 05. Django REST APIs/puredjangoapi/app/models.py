from django.db import models
from django.core.exceptions import ValidationError
from django.core.serializers import serialize

import json
import os

# Create your models here.

def validate_rating(value):
    if not (value >= 1 and value <= 5):
        raise ValidationError("Rating must be an integer between 0 and 5")

class MovieQuerySet(models.QuerySet):

    def serialize(self):
        qs = self
        json_data = serialize("json", qs, fields = ("id","title", "description", "rating", "year"))
        return json_data

class MovieManager(models.Manager):
    def get_queryset(self):
        return MovieQuerySet(self.model, using= self._db)

# Creating a model named Movie 
class Movie(models.Model):
    # Specifying the fields 
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500, null = True, blank = True)
    rating = models.IntegerField(validators= [validate_rating])
    year = models.IntegerField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add= True)

    objects = MovieManager()

    def __str__(self):
        return f'{self.id}. {self.title}'

    def serialize(self):
        json_data = serialize("json", [self], fields = ("title", "description", "rating", "year"))

        return json_data


