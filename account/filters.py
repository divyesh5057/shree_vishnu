import django_filters
from django_filters import FilterSet, AllValuesFilter
# from django_filters import DateTimeFilter, NumberFilter
from rest_framework import generics 
from django_filters.rest_framework import DjangoFilterBackend
from account.models import *

class UserFilter(django_filters.FilterSet):
    id = AllValuesFilter(field_name='id')

    username = AllValuesFilter(field_name='username')
    email    = AllValuesFilter(field_name='email')
    class Meta:
        model = User
        fields = ('id','username','email',)

class ProjectFilter(django_filters.FilterSet):
    id = AllValuesFilter(field_name='id')

    project_name = AllValuesFilter(field_name='project_name')
    class Meta:
        model = Project_db
        fields = ('id','project_name',)

class PartFilter(django_filters.FilterSet):
    id = AllValuesFilter(field_name='id')
    part_name = AllValuesFilter(field_name='part_name')
    class Meta:
        model = Parts_db
        fields = ('id','part_name',)

class TaskFilter(django_filters.FilterSet):
    id = AllValuesFilter(field_name='id')
    opretions = AllValuesFilter(field_name='opretions')
    class Meta:
        model = Task_db
        fields = ('id','opretions',)