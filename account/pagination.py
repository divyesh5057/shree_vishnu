from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
## you can override page_size, max_page_size from url query params \
## to make it more dynamic
class CustomPagination(CursorPagination):
    page_size = 5 # default page size
    ordering = 'id'
  
      
    