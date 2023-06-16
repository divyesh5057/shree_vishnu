from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
## you can override page_size, max_page_size from url query params \
## to make it more dynamic
class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100
  
      
    