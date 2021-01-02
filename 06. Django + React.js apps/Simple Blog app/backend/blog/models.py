from django.db import models
import datetime
from django.template.defaultfilters import slugify
from django.conf import settings
import shortuuid


# Create your models here.

def upload_post_image(instance, filename):
    return "post_images/{user}/{filename}".format(user = instance.user, filename = filename)

class PostQuerySet(models.QuerySet):
    pass

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using = self._db)

class PostCategories(models.TextChoices):
    TECHNOLOGY = "Technology"
    LIFESTYLE = "Lifestyle"
    ART = "Art"
    PROGRAMMING = "Programming"
    ALL = "All"
    NEWS = "News"

class BlogPost(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    user = models.ForeignKey( 
        settings.AUTH_USER_MODEL, 
        on_delete = models.SET_NULL, null = True )

    title = models.CharField(
        max_length = 200
    )

    slug = models.SlugField(max_length = 255)

    category = models.CharField(
        max_length = 200,
        choices = PostCategories.choices,
        default= PostCategories.ALL
    )

    description = models.CharField(
        max_length = 200, 
        null = True, blank = True
    )

    post_image = models.ImageField(
        upload_to = upload_post_image,
        null = True, blank = True
    )

    content = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add = True
    )

    updated = models.DateTimeField(
        auto_now = True
    )

    featured = models.BooleanField(
        default = False
    )

    objects = PostManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + '-' + str(shortuuid.ShortUUID().random(length = 10))
        
        if self.featured:
            try:
                temp = BlogPost.objects.get(featured = True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except BlogPost.DoesNotExist:
                pass

        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.id)}. {self.user.username} - {self.title}"

