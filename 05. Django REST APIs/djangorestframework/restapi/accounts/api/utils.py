# CUSTOM JWT AUTHORIZATION PAYLOAD HANDLER

from django.conf import settings
from django.utils import timezone
import datetime

expire_delta = settings.JWT_AUTH["JWT_REFRESH_EXPIRATION_DELTA"]

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user.username,  # From the JWT authorization documentation !
        ## Setting the expiration period for the token
        'expires' : timezone.now() + expire_delta - datetime.timedelta(seconds = 200) # Seconds is just as a delay !
    }