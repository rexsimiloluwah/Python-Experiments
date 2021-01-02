# Configuration files for the REST API being developed 

import datetime

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication', # JWT Authentication global configuration
        'rest_framework.authentication.SessionAuthentication'
    ], 

    'DEFAULT_PERMISSION_CLASSES' : [
        'rest_framework.permissions.IsAuthenticated'
    ], 

    'DEFAULT_PAGINATION_CLASS' : 'api.pagination.ResourcePagination',

    'DEFAULT_FILTER_BACKENDS' : [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ], 

    'SEARCH_PARAMS' : 'search',
    'ORDERING_PARAMS' : 'ordering'

}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    # 'rest_framework_jwt.utils.jwt_response_payload_handler'
    'accounts.api.utils.jwt_response_payload_handler',

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,

}