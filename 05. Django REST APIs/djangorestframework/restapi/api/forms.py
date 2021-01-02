from django import forms
from .models import Posts

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            "user",
            "content",
            "post_image"
        ]

    # Validation 
    def clean_content(self, *args, **kwargs):
        content = self.cleaned_data.get("content")
        if len(content) > 300:
            raise forms.ValidationError("Content must not be longer than 300 characters")
        return content

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        content = data.get("content", None)
        image = data.get("post_image", None)
        if content == "":
            content = None
        if content == None and image == None:
            raise forms.ValidationError("Content or Image is Required !")

        return super().clean(*args, **kwargs)