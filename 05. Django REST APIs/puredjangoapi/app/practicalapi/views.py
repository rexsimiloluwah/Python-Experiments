from django.views.generic import View
from django.http import HttpResponse

from app.models import Movie
import json
from .mixins import CSRFExemptMixin
from  app.mixins import HttpResponseMixin
from .forms import MovieModelForm
from .utilities import validate_json

# Using Class Based Views 
class MovieDetailView(HttpResponseMixin, CSRFExemptMixin, View):
    # GET
    def get(self, request, id, *args, **kwargs):

        obj = Movie.objects.get(id = id)
        if obj is None:
            error_data = json.dumps({"message" : "Object not Found !"})
            self.render_to_response(erro_data, status = 404) # 404 is used because the response resource is not found !
        
        json_data = obj.serialize()
        print(json_data)
        return HttpResponse(json_data, content_type="application/json")

    # POST
    def post(self, request, *args, **kwargs):
        response = json.dumps({
            "message" : "Method not Allowed, Please use the /api/movies endpoint"
        })
        return self.render_to_response(response, status = 405) # 405 is the status code for METHOD NOT ALLOWED 
    
    # UPDATE
    def put(self, request, id, *args, **kwargs):
        
        obj = Movie.objects.get(id = id)
        if obj is None:
            error_data = json.dumps({
                "message" : "Object not found !"
            })

            return self.render_to_response(error_data, status = 404) # 404 is used for the NOT FOUND HTTP Status code 
        
        valid_json = validate_json(request.body)
        if not valid_json:
            error_data = json.dumps({
                "message" : "Invalid Request !"
            })

            return self.render_to_response(error_data, status = 400) # 400 is used for the BAD REQUEST HTTP Status code 

        # print(json.loads(request.body))
        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body)

        for k,v in passed_data.items():
            data[0]["fields"][k] = v
        
        form = MovieModelForm(data[0]["fields"], instance = obj)

        if form.is_valid():
            obj = form.save(commit = True)
            json_data = obj.serialize()
            return self.render_to_response(json_data, status = 200) # 200 is used for a SUCCESSFUL Request
        
        elif form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_response(json_data, status = 400 ) # 400 is for BAD REQUEST

    # DELETE 
    def delete(self, request, id,  *args, **kwargs):
        obj = Movie.objects.get(id = id)
        if obj is None:
            error_data = json.dumps({
                "message" : "Object not found !"
            })

            return self.render_to_response(error_data, status = 404) # 404 is used for the NOT FOUND HTTP Status code 
        
        deleted_ = obj.delete()
        print(deleted_)
        json_data = json.dumps({
            "message" : "Deleted Successfully !"
        })
        return self.render_to_response(json_data, status = 200)  # 200 for the OK (SUCCESS) HTTP Status code

class MovieListView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def get(self,request, *args, **kwargs):
        obj = Movie.objects.filter(id__gte = 2)
        json_data = obj.serialize()
        print(json_data)
        return self.render_to_response(json_data, status = 200)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = MovieModelForm(request.POST)

        if form.is_valid():
            obj = form.save(commit = True)
            json_data = obj.serialize()
            return self.render_to_response(json_data, status = 201) #201 is for CREATED HTTP status code
        
        elif form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status = 400) # 400 is for Bad Request

        data = json.dumps({
            "message" : "NOT ALLOWED"
        })
        return self.render_to_response(data, status = 405)


    def delete(self, request, *args, **kwargs):
        data = json.dumps({
            "message" : "Forbidden Request"
        })
        return self.render_to_response(data, status = 403)
    
