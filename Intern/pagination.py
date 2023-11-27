
from Intern.serializer import BookSeralizer
from Intern.models import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class MyPagination(PageNumberPagination):
    # page_size=5
    page_query_param='page'
    page_size_query_param='records'