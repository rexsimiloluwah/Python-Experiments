"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from app.views import *
from app.practicalapi.views import MovieDetailView, MovieListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^movie/', movie_view), 
    url(r'^jsonmixinview/', JsonCBV.as_view()), 
    url(r'^serializeddetailview/', SerializedDetailView.as_view()),
    url(r'^serializedlistview/', SerializedListView.as_view()),
    url(r'^serializedlistviewcustom/', SerializedListViewCustom.as_view()),
    url(r'^api/movies/(?P<id>\d+)$', MovieDetailView.as_view()),
    url(r'^api/movies', MovieListView.as_view())

]
