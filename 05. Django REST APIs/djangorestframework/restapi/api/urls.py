from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from api.views import PostListAndSearchView, PostSearchView, PostCreateView

urlpatterns = [
    url(r'^', PostSearchView.as_view()),
    url(r'^create/$', PostCreateView.as_view())
]