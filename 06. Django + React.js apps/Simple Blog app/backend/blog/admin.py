from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import BlogPost

# Apply summernote to all TextField in model.
class BlogPostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    exclude = ['slug']
    list_display = (
        'id',
        'user',
        'title',
        'timestamp'
    )
    list_display_links = (
        'id',
        'title'
    )
    summernote_fields = (
        'content'
    )

admin.site.register(BlogPost, BlogPostAdmin)