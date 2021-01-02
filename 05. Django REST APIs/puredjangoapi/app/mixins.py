# A Mixin is a special kind of class in Python , that allows any class that inherits from the Mixin to share methods with it
# A Mixin is primarily used in Class Based Views 

from django.http import JsonResponse, HttpResponse

class JsonResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        """
            This function basically renders a JSON response
        """
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context): 
        return context

class HttpResponseMixin(object):

    is_json = False

    def render_to_response(self, data, status = 200):
        content_type = "text/html"
        if self.is_json:
            content_type = "application/json"
        return HttpResponse(data, content_type= content_type, status = status)

