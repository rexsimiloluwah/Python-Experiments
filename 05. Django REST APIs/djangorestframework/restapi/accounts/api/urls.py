from django.urls import path
from django.conf.urls import url, include

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import AuthAPIView, RegisterAPIView, RegisterAPIViewSerialized

urlpatterns = [
    url(r'^login$', AuthAPIView.as_view()),
    url(r'^register', RegisterAPIView.as_view()), 
    url(r'^serializedregister', RegisterAPIViewSerialized.as_view()),
    url(r'^jwt/$', obtain_jwt_token), 
    url(r'^jwt/refresh/$', refresh_jwt_token),
    # url(r'^api/posts/(?P<pk>\d+)/update/$', PostUpdateView.as_view()),
    # url(r'^api/posts/(?P<pk>\d+)/delete/$', PostDeleteView.as_view()),
]