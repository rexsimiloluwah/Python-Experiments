from django import forms 
from app.models import Movie

class MovieModelForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "title",
            "description",
            "rating",
            "year"
        ]