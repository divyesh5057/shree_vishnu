from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import * #UserLoginSerializer, UserRegistrationSerializer, UserlogoutSerializer,ProjectSerializer,PartSerializer,TaskSerializer,TimesheetSerializer,UserGetAll,ProjectGetSerializer,PratsGetSerializer,TaskGetSerializer
from django.contrib.auth import authenticate, logout,login
from account.models import *
from datetime import datetime
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .pagination import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import *
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from rest_framework import viewsets
from account.task import create_random_user_accounts
from datetime import date
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from .models import Inventory_db
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from tempfile import NamedTemporaryFile
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, LongTable, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from tempfile import NamedTemporaryFile
from django.urls import reverse
from django.urls import reverse
import os
from django.conf import settings
import re
from .permissions import IsAdminOrReadOnly, IsAdmin
from rest_framework.parsers import MultiPartParser
import json
from .models import secondary_inventory_stock
from django.db import transaction
from django.shortcuts import get_object_or_404


class UserRegistrationView(APIView):
    """ 
        Register User....
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    serializer_class = UserRegistrationSerializer
    def get(self,request,format=None):
        user = User.objects.all()
        serializer = UserGetAll(user,many=True, context={'request':request})
        return Response(serializer.data,status=status.HTTP_201_CREATED)

   
    def post(self,request,):
        serializer = self.serializer_class(data=request.data)
        username = request.data.get('username', None)  # Use the get() method to retrieve the username value
        password = request.data.get('password', None)
        if serializer.is_valid():
            user=serializer.save()
            authenticate(username=username, password=password)
            login(request,user)
            token = Token.objects.get_or_create(user=user)[0].key
            response={
                    'token':token,
                    'msg':'User Registered Successfully',
                    'status':True
                }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
    def put(self, request,id,):
        # id = request.data.get('check_in')
        user = User.objects.get(id=id)
        serializer = UserGetAll(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        try:
            user = User.objects.get(id=id) 
            user.delete()
            return Response({"msg":" User deleted successfully "},status=status.HTTP_201_CREATED)
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------Get_users Model ----------------------------------------------------------------
class Get_users(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer = UserGetAll(users, many=True)
        return Response(serializer.data)
# ----------------------------------UserLoginView Model ----------------------------------------------------------------
class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user =User.objects.filter(username=username).first()
            if user:
                user.is_active=True
                user.save()
                user_ = authenticate(username=username, password=password)
                user_type = User.objects.get(username=username)
                if user_:
                    token = Token.objects.get_or_create(user=user)[0].key
                    response={
                                'token':token,
                                'msg':'Login Success',
                                'status':True,
                                'username':username,
                                'usertype':user_type.role,
                                'userid':user_type.id
                            }
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    return Response({'msg':'Password is not valid'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'msg':"Username is not valid"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg':'username or password is not valid'}, status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------AdminLoginView Model ----------------------------------------------------------------
class AdminLoginView(APIView):
    def post(self, request, format=None):
        user = request.user 
        username = request.data.get('username')

        try:
            get_user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Return an error response if the user is not found
            error_message = f"The user '{username}' was not found."
            response_data = {'error': error_message}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        if get_user.role == 'Employee':
            response = {
                'msg': 'You cannot log in to this admin site.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                username = serializer.data.get('username')
                password = serializer.data.get('password')
                user =User.objects.filter(username=username).first()
                if user:
                    user.is_active=True
                    user.save()
                    user_ = authenticate(username=username, password=password)
                    user_type = User.objects.get(username=username)
                    if user_:
                        token = Token.objects.get_or_create(user=user)[0].key
                        response={
                                    'token':token,
                                    'msg':'Login Success',
                                    'status':True,
                                    'username':username,
                                    'usertype':user_type.role
                                }
                        return Response(response, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'msg':'Password is not valid'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'msg':"Username is not valid"}, status=status.HTTP_404_NOT_FOUND)
            return Response({'msg':'username or password is not valid'}, status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------UserLogoutView Model ----------------------------------------------------------------
class UserLogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response({'mag':'User Logged out successfully'},status=status.HTTP_201_CREATED)
# ----------------------------------PrimaryInventoryView Model ----------------------------------------------------------------
class PrimaryInventoryView(generics.CreateAPIView):
    queryset = primary_inventory.objects.all()
    serializer_class = PrimaryInventorySerializer
# ----------------------------------ProjectAllDBView Model ----------------------------------------------------------------
class ProjectAllDBView(APIView):
    def get(self, request):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)

        if get_user.role == 'Subadmin':
            user = Project_db.objects.all()
            serializer = ProjectsDBSubAdminSerializer(user,many=True)
            return Response({"msg":serializer.data},status=status.HTTP_201_CREATED)
        else:
            user = Project_db.objects.all()
            serializer = ProjectsDBAdminSerializer(user,many=True)
            return Response({"msg":serializer.data},status=status.HTTP_201_CREATED)

# ----------------------------------ProjectDBView Model ----------------------------------------------------------------
class ProjectDBView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    def get(self, request, pk=None):
        users = request.user
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)

        if get_user.role == 'Subadmin':
            if pk is not None:
                # Get a single project with the specified ID
                project = get_object_or_404(Project_db, pk=pk)
                serializer = ProjectsDBSubAdminSerializer(project)
                return Response(serializer.data)
            else:
                # Get all projects
                user = Project_db.objects.all()
                paginator = CustomPagination()
                result_page = paginator.paginate_queryset(user, request)
                serializer = ProjectsDBSubAdminSerializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
        else:
            if pk is not None:
                # Get a single project with the specified ID
                project = get_object_or_404(Project_db, pk=pk)
                serializer = ProjectsDBAdminSerializer(project)
                return Response(serializer.data)
            else:
                # Get all projects
                user = Project_db.objects.all()
                paginator = CustomPagination()
                result_page = paginator.paginate_queryset(user, request)
                serializer = ProjectsDBAdminSerializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)


    def post(self, request):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAdminUser]
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg': "You don't have authority to add any project.",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ProjectDBSerializer(data=request.data)
            emp_data = request.data.get('emp', [])
            secondary_inventory = request.data.get('secondary_inventory', [])

            primary_inventory_data = request.data.get('primary_inventory', [])
            stock_data = request.data.get('stock', [])  # Retrieve stock data
            # customer_id = request.data.get('customer_id')

            if serializer.is_valid():
                with transaction.atomic():
                    project = serializer.save()

                    project.emp.set(emp_data)
                    project.secondary_inventory.set(secondary_inventory)

                    for item in primary_inventory_data:
                        supplier_ids = item.get('supplier', [])
                        name = item.get('inventoryName')

                        primary_inv = primary_inventory.objects.create(
                            project_id=project,
                            name=name
                        )
                        primary_inv.supplier_id.set(supplier_ids)

                    for stock_item in stock_data:
                        inventory_id = stock_item.get('inventory_id')
                        stock_quantity = stock_item.get('stock_quantity')

                        try:
                            inventory = Inventory_db.objects.get(id=inventory_id)
                        except Inventory_db.DoesNotExist:
                            return Response(
                                f"Inventory with ID {inventory_id} not found.",
                                status=status.HTTP_404_NOT_FOUND
                            )

                        current_stock_quantity = int(inventory.stock_quantity)
                        updated_stock_quantity = current_stock_quantity - int(stock_quantity)

                        if updated_stock_quantity < 0:
                            response = {
                                'msg': f"Insufficient stock. Available stock quantity for inventory {inventory_id} is {current_stock_quantity}.",
                            }
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)

                        inventory.stock_quantity = str(updated_stock_quantity)
                        inventory.save()

                        secondary_stock, created = secondary_inventory_stock.objects.get_or_create(
                            project_id=project,
                            secondary_inventory=inventory
                        )
                        secondary_stock.stock_quantity = stock_quantity
                        secondary_stock.save()

                    response = {
                        'msg': 'Projects details added',
                        'status': True
                    }
                    return Response(response, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
    def put(self, request, pk):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response = {
                'msg': "You don't have authority to update any project.",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                project = Project_db.objects.get(pk=pk)
            except Project_db.DoesNotExist:
                return Response(f"Project with ID {pk} not found.", status=status.HTTP_404_NOT_FOUND)

            serializer = ProjectDBSerializer(project, data=request.data)
            emp_data = request.data.get('emp', [])
            primary_inventory_data = request.data.get('primary_inventory', [])
            secondary_inventory_data = request.data.get('secondary_inventory', [])
            stock_data = request.data.get('stock', [])

            if serializer.is_valid():
                with transaction.atomic():
                    serializer.save()

                    project.emp.set(emp_data)

                    # Update primary inventory
                    primary_inventories = primary_inventory.objects.filter(project_id=project)
                    primary_inventory_ids = set(primary_inventories.values_list('id', flat=True))

                    # Delete primary inventories not included in the request
                    inventories_to_delete = primary_inventory_ids - set(
                        item.get('inventoryName') for item in primary_inventory_data
                    )
                    primary_inventory.objects.filter(id__in=inventories_to_delete).delete()

                    # Create or update primary inventories from the request data
                    for item in primary_inventory_data:
                        supplier_ids = item.get('supplier', [])
                        name = item.get('inventoryName')

                        primary_inv, _ = primary_inventory.objects.get_or_create(
                            project_id=project,
                            name=name
                        )
                        primary_inv.supplier_id.set(supplier_ids)

                    # Update secondary inventory
                    secondary_inventories = secondary_inventory_stock.objects.filter(project_id=project)
                    secondary_inventory_ids = set(secondary_inventories.values_list('id', flat=True))

                    # Delete secondary inventories not included in the request
                    inventories_to_delete = secondary_inventory_ids - set(secondary_inventory_data)
                    secondary_inventory_stock.objects.filter(id__in=inventories_to_delete).delete()

                    # Create or update secondary inventories from the request data
                    # for inventory_id in secondary_inventory_data:
                    #     try:
                    #         secondary_inventory = secondary_inventory_stock.objects.get(id=inventory_id)
                    #     except secondary_inventory_stock.DoesNotExist:
                    #         return Response(
                    #             f"Secondary inventory with ID {inventory_id} not found.",
                    #             status=status.HTTP_404_NOT_FOUND
                    #         )
                    #     secondary_inventory.project_id = project
                    #     secondary_inventory.save()

                    # Update stock
                    for stock_item in stock_data:
                        inventory_id = stock_item.get('inventory_id')
                        stock_quantity = stock_item.get('stock_quantity')

                        try:
                            secondary_inventory = Inventory_db.objects.get(id=inventory_id)
                        except Inventory_db.DoesNotExist:
                            return Response(
                                f"Secondary inventory with ID {inventory_id} not found.",
                                status=status.HTTP_404_NOT_FOUND
                            )

                        current_stock_quantity = int(secondary_inventory.stock_quantity)
                        updated_stock_quantity = current_stock_quantity - int(stock_quantity)

                        if updated_stock_quantity < 0:
                            response = {
                                'msg': f"Insufficient stock. Available stock quantity for inventory {inventory_id} is {current_stock_quantity}.",
                            }
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)

                        secondary_inventory.stock_quantity = str(updated_stock_quantity)
                        secondary_inventory.save()

                        secondary_stock, _ = secondary_inventory_stock.objects.get_or_create(
                            project_id=project,
                            secondary_inventory=secondary_inventory
                        )
                        secondary_stock.stock_quantity = stock_quantity
                        secondary_stock.save()

                    response = {
                        'msg': 'Project updated successfully',
                        'status': True
                    }
                    return Response(response, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, pk):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':"You don't have authority to delete any project.",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                project = Project_db.objects.get(pk=pk)
            except Project_db.DoesNotExist:
                return Response(f"Project with ID {pk} not found.", status=status.HTTP_404_NOT_FOUND)

            project.delete()
            response={
                        'msg':'"Data delete successfully',
                        'status':True

                            }
            return Response(response,status=status.HTTP_201_CREATED)
# ----------------------------------ProjectUsers Model ----------------------------------------------------------------
class ProjectUsers(APIView):
    def get(self,request, format=None):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAuthenticated]
        current_user=request.user.id
        user = Project_db.objects.filter(emp__id=current_user)
        serializer = Project_GetSerializer(user,many=True)
        serializer=serializer.data
        return Response(serializer, status=status.HTTP_201_CREATED)
# ----------------------------------PartslistView Model ----------------------------------------------------------------
class PartslistView(APIView):
    def get(self, request, id, format=None):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        current_user = request.user.id

        print("Project ID:", id)

        parts = Parts_db.objects.filter(project_id__id=id)
        if not parts:
            return Response({'message': 'No parts are assigned to this project ID.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = Part_list_Serializer(parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# ----------------------------------Parts_TaskListView Model --------------------------------------------------------------
class Parts_TaskListView(APIView):
    def get(self, request, id, format=None):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        current_user = request.user.id


        tasks = Task_db.objects.filter(parts_id__id=id)
        
        part_ids = [task.parts_id.id for task in tasks]
        part_description = Parts_db.objects.filter(id__in=part_ids).values_list('part_description', flat=True)

        if not tasks:
            return Response({'message': 'No tasks are assigned to this parts ID.'}, status=status.HTTP_404_NOT_FOUND)

        if not part_description:
            return Response({'message': 'No part description found for the given tasks.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(tasks, many=True)
        
        response_data = {
            'part_description': list(part_description),
            'tasks': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
# ----------------------------------UpdatePartsView Model --------------------------------------------------------
class UpdatePartsView(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,reuest,format=None):
        user = Parts_db.objects.all()
        serializer = PratsGetSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':"You don't have authority to update any Parts.",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            user = Parts_db.objects.get(id=id)
            print('dgf',user)
            serializer = PratsGetSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self,request,id,format=None):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':"You don't have authority to delete any Parts.",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = Parts_db.objects.get(id=id) 
                user.delete()
                return Response({"msg":" Part deleted successfully "},status=status.HTTP_201_CREATED)  
            except:
                return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------PartsView Model --------------------------------------------------------
class PartsView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,request, format=None):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAuthenticated]
        user = Parts_db.objects.all()
        serializer = PartSerializer(user,many=True)
        serializer=serializer.data
        return Response(serializer, status=status.HTTP_201_CREATED)
    
    def post(self, request, format=None):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':"You don't have authority to add any Parts.",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PratsGetSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response={
                    'msg':'Parts details add',
                    'data':serializer.data,
                    'status':True
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------Get_part Model --------------------------------------------------------
class Get_part(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = Parts_db.objects.all()
        serializer = PartImgDocSerializer(users, many=True)
        return Response(serializer.data)
# ----------------------------------UpdateTaskView Model --------------------------------------------------------
class UpdateTaskView(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,reuest,format=None):
        user = Task_db.objects.all()
        serializer = TaskGetSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':"You don't have authority to update any Task.",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            user = Task_db.objects.get(id=id)
            print('dgf',request.data)
            serializer = TaskaddSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response={
                    'msg':'Task details updated',
                    'data':serializer.data,
                    'status':True
                }
                return Response(response,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':"You don't have authority to delete any Task.",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = Task_db.objects.get(id=id) 
                user.delete()
                return Response({"msg":" Task deleted successfully "},status=status.HTTP_201_CREATED)   
            except:
                return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------TaskView Model --------------------------------------------------------
class TaskView(APIView):
    def post(self, request, format=None):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAdminUser]
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':"You don't have authority to add any Task.",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            authentication_classes=[TokenAuthentication]
            permission_classes=[IsAdminUser]
            serializer = TaskaddSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                data = serializer.save()
                response={
                    'msg':'Task assigned successfully',
                    'data':serializer.data,
                    'status':True
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        current_user = request.user.id
        today = date.today()
        user = Task_db.objects.filter(emp_id=current_user, created_date__date=today)
        serializer = TaskSerializer(user, many=True)
        serializer_data = serializer.data
        return Response(serializer_data, status=status.HTTP_200_OK)
# ----------------------------------TaskViewUser Model ---------------------------------------
class TaskViewUser(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        serializer = TaskaddSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            response={
                'msg':'Task assigned successfully',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        task = Task_db.objects.get(id=id)
        serializer = TaskaddSerializer(task, data=request.data)
        if serializer.is_valid():
            # Check if working_status is updated to "complete"
            old_working_status = task.working_status
            new_working_status = request.data.get('working_status')
            if old_working_status != new_working_status and new_working_status == 'Complete':
                print("i m if")
                task.is_task = True
            elif  old_working_status == new_working_status and new_working_status == 'Complete':
                task.is_task = True
            else:
                task.is_task = False

            # Calculate the new total_hours value
            old_total_hours = int(task.total_hours)
            new_total_hours = int(request.data.get('total_hours', 0))
            updated_total_hours = old_total_hours + new_total_hours

            # Update the serializer data
            serializer.validated_data['total_hours'] = str(updated_total_hours)
            serializer.save()

            response = {
                'msg': 'Task details updated',
                'data': serializer.data,
                'status': True
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        try:
            user = Task_db.objects.get(id=id) 
            user.delete()
            return Response({"msg":" Task deleted successfully "},status=status.HTTP_201_CREATED)   
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------InventoryView Model ---------------------------------------
class InventoryView(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    def post(self, request, format=None):
        serializer = InventoryAllSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response={
                'msg':'Inventory add',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        user = Inventory_db.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(user, request)
        serializer = InventoryAllSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def put(self, request,id,):
        user = Inventory_db.objects.get(id=id)
        serializer = InventoryAllSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'msg':'Inventory updated',
                'data':serializer.data,
                'status':True
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id,format=None):
        try:
            user = Inventory_db.objects.get(id=id) 
            user.delete()
            return Response({"msg":" Inventory deleted successfully "},status=status.HTTP_201_CREATED)   
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------TransporterView Model ---------------------------------------
class TransporterView(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    def post(self, request, format=None):
        serializer = TransporterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response={
                'msg':'Transporter add',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,reuest,format=None):
        user = Transporter_db.objects.all()
        serializer = TransporterSerializer(user,many=True)
        return Response(serializer.data,status=200)
    
    def put(self, request,id,):
        user = Transporter_db.objects.get(id=id)
        serializer = TransporterSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'msg':'Transporter updated',
                'data':serializer.data,
                'status':True
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id,format=None):
        try:
            user = Transporter_db.objects.get(id=id) 
            user.delete()
            return Response({"msg":" Transporter deleted successfully "},status=status.HTTP_201_CREATED)   
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------User Profile ---------------------------------------

class UserProfileAPIView(APIView): 
    """ 
       An endpoint for User Retrieve,Update and Delete 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]  
    def get(self,request):
        try:
            user_id=request.user.id
            
            user = User.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data,status=201)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request,):
        try:
            user_id=request.user.id
            user = User.objects.get(id=user_id)
            data=request.data
            serializer = UserProfileSerializer(user,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
# -----------------------------------TotalCountAPIView Model --------------------------------------  
class TotalCountAPIView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    def get(self, request):
        user_count = User.objects.count()
        inventory_count = Inventory_db.objects.count()
        supplier_count = Supplier_db.objects.count()
        project_count = Project_db.objects.count()

        counts = {
            'user_count': user_count,
            'inventory_count': inventory_count,
            'supplier_count': supplier_count,
            'project_count': project_count,
        }

        return Response(counts)
# -----------------------------------Project_view Model --------------------------------------
class Project_view(APIView):
    def get(self, request, format=None):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAdminUser]
        
        paginator = CustomPagination()
        tasks = Task_db.objects.all()
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        
        serializer = TaskSerializer(paginated_tasks, many=True)
        
        return paginator.get_paginated_response( serializer.data)
# -----------------------------------PDF Model --------------------------------------
def download_pdf(request, filename):
    # Get the file path
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Create a response with file content as attachment
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    return response

def format_table_row(row):
    nested_data = []
    if isinstance(row, dict):
        for key, value in row.items():
            if isinstance(value, list):
                nested_data.append([key, ""])
                for item in value:
                    nested_data.extend(format_table_row(item))
            elif isinstance(value, dict):
                nested_data.append([key, ""])
                nested_data.extend(format_table_row(value))
            else:
                nested_data.append([key, value])
    else:
        nested_data.append(["", row])

    return nested_data

def create_pdf(data, project_name):
    # Generate the PDF filename with project name and today's date
    today = date.today().strftime("%Y-%m-%d")
    filename = f"{project_name}_{today}.pdf"

    # Create the PDF document with landscape orientation and increased height
    doc = SimpleDocTemplate(filename, pagesize=landscape(letter), bottomMargin=30)
    elements = []

    # Add table data
    table_data = []
    for item in data[0]:
        table_data.extend(format_table_row({item: data[0][item]}))

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alignment
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), 'white'),  # Table row background color
        ('GRID', (0, 0), (-1, -1), 1, 'black'),  # Grid lines
    ])

    table = Table(table_data, style=table_style)
    elements.append(table)
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Create the PDF document with landscape orientation and increased height
    doc = SimpleDocTemplate(file_path, pagesize=landscape(letter), bottomMargin=30)
    doc.build(elements)

    return filename

class projectdata_pdf(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':"You don't have authority to download.",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            project_names = request.data.get('project_name', [])
            # Retrieve the data for each project name

            project_data = Project_db.objects.filter(project_name=project_names).prefetch_related('parts_db_set__emp_id')
            if not project_data:
                # Return an error response if the project is not found
                error_message = f"The project '{project_names}' was not found."
                response_data = {'error': error_message}
                return JsonResponse(response_data, status=404)

            inventory_data = []
            for project in project_data:
                parts_info = []
                for part in project.parts_db_set.all():
                    tasks_info = []
                    for task in part.task_db_set.all():
                        try:
                            emp_info = task.emp_id.username
                        except AttributeError:
                            emp_info = None
                        # print( task.emp_id.username)
                        
                        tasks_info.append({
                            'opretions': task.opretions,
                            'working_status': task.working_status,
                            'total_hours': task.total_hours,
                            'is_poverty': task.is_poverty,
                            'created_date': task.created_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'updated_date': task.updated_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'is_role': task.is_role,
                            'is_task': task.is_task,
                            'emp_info': emp_info,
                        })
                    
                    # emp_info = [emp.username for emp in part.emp_id.all()]
                    emp_info = [emp.username for emp in part.emp_id.all() if emp is not None]
                    parts_info.append({
                        'part_name': part.part_name,
                        'working_status': part.working_status,
                        'part_description': part.part_description,
                        # 'total_hours': part.total_hours,
                        'created_at': part.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'updated_at': part.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'part_doc': part.part_doc.url if part.part_doc else None,
                        'emp_list': emp_info,
                        # 'tasks': tasks_info,

                    })
                emp_info = [emps.username for emps in project.emp.all() if emps is not None]
                project_info = {
                    'project_name': project.project_name,
                    'project_pricing': project.project_pricing,
                    'working_status': project.working_status,
                    'project_description': project.project_description,
                    'emp_list': emp_info,
                    'parts': parts_info,
                }
                inventory_data.append(project_info)
            # ...

            # Generate the PDF with project data
            pdf_filename = create_pdf(inventory_data, project_names)  # Assuming project_names contains only one project

            # Create the download URL for the PDF
            download_url = reverse('download_pdf', kwargs={'filename': pdf_filename})

            # Create the response with the download URL
            response_data = {'url': download_url}
            response = JsonResponse(response_data, status=200)

            return response
# -----------------------------------Supplier Model --------------------------------------
class Supplier(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    serializer_class = SupplierSerializer
    pagination_class = CustomPagination
    
    def get(self, request):
        suppliers = Supplier_db.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(suppliers, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Supplier added successfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            customer = Supplier_db.objects.get(pk=pk)
        except Supplier_db.DoesNotExist:
            return Response({'error': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Supplier updated successfully', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            customer = Supplier_db.objects.get(pk=pk)
        except Supplier_db.DoesNotExist:
            return Response({'error': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)
        
        customer.delete()
        return Response({'message': 'Supplier deleted successfully'}, status=status.HTTP_200_OK)
    
# -----------------------------------Customer Model --------------------------------------
class Customer(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    serializer_class = CustomerSerializer
    pagination_class = CustomPagination
    
    def get(self, request):
        customers = Customer_db.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(customers, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Customer added successfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            customer = Customer_db.objects.get(pk=pk)
        except Customer_db.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Customer updated successfully', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            customer = Customer_db.objects.get(pk=pk)
        except Customer_db.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        
        customer.delete()
        return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_200_OK)
            

#Gwt api for all withi pagination -------------------    
class Getusers(ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserGetAll
    pagination_class = CustomPagination

class Getpart(ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = Parts_db.objects.all()
    serializer_class = PartImgDocSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        queryset = Parts_db.objects.all()
        task_id = self.request.query_params.get('id')
        if task_id:
            queryset = queryset.filter(id=task_id)
        return queryset
    
class Gettask(ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = Task_db.objects.all()
    serializer_class = TaskallSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        queryset = Task_db.objects.all()
        task_id = self.request.query_params.get('id')
        if task_id:
            queryset = queryset.filter(id=task_id)
        return queryset
    
class Get_task(ListAPIView):
    # def get(self,reuest,format=None):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = Task_db.objects.all()
        serializer = TaskallSerializer(users, many=True)
        return Response(serializer.data)
    
 # Filter api for all ---------------------------------   
class FilterUsers(generics.ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserGetAll
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter  

class FilterProject(generics.ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = Project_db.objects.all()
    serializer_class = ProjectsDBAdminSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter  

class FilterPart(generics.ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = Parts_db.objects.all()
    serializer_class = PratsGetSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartFilter 

class FilterTask(generics.ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = Task_db.objects.all()
    serializer_class = TaskGetSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter 