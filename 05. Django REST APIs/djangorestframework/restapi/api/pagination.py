from rest_framework import pagination

class ResourcePagination(pagination.PageNumberPagination):
    page_size =    5