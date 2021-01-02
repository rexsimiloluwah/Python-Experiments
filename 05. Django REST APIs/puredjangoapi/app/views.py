from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.core.serializers import serialize

# Import models 
from .models import Movie

# Import Mixins 
from .mixins import JsonResponseMixin
# Other helpers 
import os 
import json

# Create your views here.

def movie_view(request):
    data = {
        "count" : 10, 
        "country" : "Seychelles"
    }

    return JsonResponse(data)

# -- JSON Class Based View --

# Json response using the JSON response mixin 

class JsonCBV(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs ):
        
        data = {
            "Number of Cases" : 1000, 
            "Country" : "United States of America"
        }

        return self.render_to_json_response(data)

# Serializing single data
class SerializedDetailView(JsonResponseMixin, View):
    """
        Serialized Detail View is used to serialize a single object of data
    """
    def get(self, request, *args, **kwargs):
        obj = Movie.objects.get(id = 1)
        data = {
            "Title" : obj.title, 
            "Description" : obj.description, 
            "Rating" : obj.rating, 
            "Year" : obj.year, 
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type = "application/json")

# Serializing a list of data
class SerializedListView(View):
    """
        Serialized List View is used to serialize an array of data objects
    """
    def get(self, request, *args, **kwargs):
        obj = Movie.objects.all()
        data = serialize("json", obj)
        print(data)

        json_data = data
        return HttpResponse(data, content_type="application/json")

# Using a custom serializer 
class SerializedListViewCustom(View):

    def get(self, request, *args, **kwargs):
        obj = Movie.objects.all()
        print(obj.serialize())
        return HttpResponse(obj.serialize(), content_type="application/json")