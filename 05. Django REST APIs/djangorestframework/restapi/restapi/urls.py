"""restapi URL Configuration

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
from api.views import PostListAndSearchView, PostSearchView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^api/posts/$', PostSearchView.as_view()),
    url(r'^api/posts/(?P<pk>\d+)/$', PostDetailView.as_view()),
    url(r'^api/auth/', include('accounts.api.urls')), 
    url(r'^api/users/', include('accounts.users.urls'))
    # url(r'^api/posts/(?P<pk>\d+)/update/$', PostUpdateView.as_view()),
    # url(r'^api/posts/(?P<pk>\d+)/delete/$', PostDeleteView.as_view()),
]
