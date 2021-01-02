from django.db import models
from django.conf import settings

# Create your models here.

class TodoQuerySet(models.QuerySet):
    pass

class TodoManager(models.Manager):
    def get_queryset(self):
        return TodoQuerySet(self.model, using = self._db)

class PriorityCategories(models.TextChoices):
    HIGH = "High"
    LOW = "Low"
    NORMAL = "Normal"
    

class Todo(models.Model):

    id = models.AutoField(
        primary_key = True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL, null = True
    )

    title = models.CharField(
        max_length = 200
    )

    description = models.CharField(
        max_length = 500
    )

    timestamp = models.DateTimeField(
        auto_now_add = True
    )

    updated = models.DateTimeField(
        auto_now = True
    )

    completed = models.BooleanField(
        default = False
    )

    priority = models.CharField(
        max_length = 50,
        choices = PriorityCategories.choices,
        blank = True, 
        null = True,
        default = 'Normal'
    )

    objects = TodoManager()

    def __str__(self):
        return f"{self.id} - {self.title}"