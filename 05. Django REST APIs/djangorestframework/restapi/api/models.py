from django.db import models
from django.conf import settings
# Create your models here.

def upload_post_image(instance, filename):
    return "posts/{user}/{filename}".format(user = instance.user, filename = filename)

class PostQuerySet(models.QuerySet):
    pass

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using = self._db)

# Model for Posts
class Posts(models.Model):
    id = models.AutoField( primary_key = True)
    user = models.ForeignKey( 
        settings.AUTH_USER_MODEL, 
        on_delete = models.SET_NULL, null = True )
    content = models.CharField(max_length=300, null = True, blank = True)
    post_image = models.ImageField(upload_to = upload_post_image, null = True, blank = True)
    updated = models.DateTimeField(auto_now = True) # auto_now updates the value of the field every time a Model.save() method is called
    timestamp = models.DateTimeField(auto_now_add = True) #auto_now_add updates only when the model is created

    objects = PostManager()

    def __str__(self):
        return f'{self.id}. {str(self.user.username)} - {str(self.updated)}'

    class Meta:
        verbose_name = "Posts"
        verbose_name_plural = "Posts"

    @property
    def owner(self):
        return self.user

    