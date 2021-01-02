from django.contrib import admin

# Register your models here.
from .models import Posts

from .forms import PostForm

class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "__str__", "post_image"]
    form = PostForm

admin.site.register(Posts, PostAdmin)