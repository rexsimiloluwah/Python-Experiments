from django.urls import path
from django.conf.urls import url, include

from .views import UserDetailAPIView, PostUserAPIView

urlpatterns = [
    url(r'^(?P<username>\w+)/$', UserDetailAPIView.as_view(), name="UserDetailApiView"),
    url(r'^(?P<username>\w+)/posts/$', PostUserAPIView.as_view(), name="PostUserAPIView"),
]