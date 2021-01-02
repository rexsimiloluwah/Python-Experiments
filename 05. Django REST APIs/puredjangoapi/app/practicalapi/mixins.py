# This mixin is to prevent the CSRF (Cross-site resource forgery) error that occurs during post requests 

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator # To apply a method decorator to a particular method 

class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self , *args, **kwargs):
        return super().dispatch(*args, **kwargs)


