from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from app.views import *

from app.practicalapi.views import *

urlpatterns = [
    url(r'^', MovieListView.as_view()),
    url(r'^(?P<id>\d+)$',  MovieDetailView.as_view()), 
]
