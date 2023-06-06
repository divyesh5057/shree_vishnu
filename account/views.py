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

# Create your views here.

class UserRegistrationViews(APIView):
    # permission_classes = [IsAdminOrReadOnly]  # Allow read access for subadmin, full access for admin

    def post(self, request):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    
    """ 
        Register User....
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    serializer_class = UserRegistrationSerializer
    def get(self,request,format=None):
        user = User.objects.all()
        # page_number = self.request.query_params.get('page_number ', 1)
        # page_size = self.request.query_params.get('page_size ', 5)

        # paginator = Paginator(user , page_size)
        # pagination_class = CustomPagination
        
        serializer = UserGetAll(user,many=True, context={'request':request})
        return Response(serializer.data,status=status.HTTP_201_CREATED)

   
    def post(self,request,):
        serializer = self.serializer_class(data=request.data)
        print(">>>>>>>>>",request.data) 
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


class UserLoginView(APIView):
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
   
        # obj =  User.objects.filter(id=request.use)
        # for j in obj:
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
    
class AdminLoginView(APIView):
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAdminUser]
    def post(self, request, format=None):
        users = request.user 
        usernames = request.data.get('username')
        get_user = User.objects.get(username=usernames)
        print(get_user.role)
        if get_user.role == 'Employee':
            response={
                'msg':'You can not login this admin site ',
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
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

class UserLogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response({'mag':'User Logged out successfully'},status=status.HTTP_201_CREATED)
      

class GetAllProject(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    # permission_classes = [IsAdminOrReadOnly]
    def get(self, request, format=None):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)

        if get_user.role == 'Subadmin':
            subadmin = ProjectGetSerializerSubadmin
            user = Project_db.objects.all()
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(user, request)
            serializer = ProjectGetSerializerSubadmin(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            user = Project_db.objects.all()
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(user, request)
            serializer = ProjectGetSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)


class UpdateProjects(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,reuest,format=None):
        user = Project_db.objects.all()
        serializer = ProjectGetSerializer(user,many=True)
        return Response({"msg":serializer.data},status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        # id = request.data.get('check_in')
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':'You can not update any data ',
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:    
            user = Project_db.objects.get(id=id)
            print('dgf',id)
            serializer = ProjectSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            # return Response("Project updated successfully ")
    
    def delete(self,request,id,format=None):
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':'You can not delete any data ',
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = Project_db.objects.get(id=id) 
                user.delete()
                return Response({"msg":" Project deleted successfully "}, status=status.HTTP_201_CREATED)
            except :
                print("fff")
                return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)


class ProjectView(APIView):
   
    def get(self,request, format=None):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAuthenticated]
        current_user=request.user.id
        user = Project_db.objects.filter(emp__id=current_user)
        serializer = ProjectGetSerializer(user,many=True)
        serializer=serializer.data
        return Response(serializer, status=status.HTTP_201_CREATED)

        
    def post(self, request, format=None):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAdminUser]
        users = request.user 
        get_user = User.objects.get(pk=str(users))
        print(get_user.role)
        if get_user.role == 'Subadmin':
            response={
                'msg':'You can not add any data ',
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response={
                    'msg':'Projects deatails add',
                    'data':serializer.data,
                    'status':True
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectImgDocView(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def post(self, request, format=None):
        serializer = ProjectimgdocSendSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response={
                'msg':'Data add successfully',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,reuest,format=None):
        user = Project_img_doc.objects.all()
        serializer = ProjectimgdocSendSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        user = Project_img_doc.objects.get(id=id)
        print('dgf',user)
        serializer = ProjectimgdocSendSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'msg':'Data update successfully',
                'data':serializer.data,
                'status':True
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self,request,id,format=None):
        try:
            user = Project_img_doc.objects.get(id=id) 
            user.delete()
            return Response({"msg":"Data delete successfully "},status=status.HTTP_201_CREATED)  
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
class GetAllProjects(APIView):
    def get(self,request, format=None):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAuthenticated]
        user = Project_db.objects.all()
        serializer = GetProjectSerializer(user,many=True)
        serializer=serializer.data
        return Response(serializer, status=status.HTTP_201_CREATED)
    
class PartImgDocView(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def post(self, request, format=None):
        serializer = PartimgdocSendSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response={
                'msg':'Data add successfully',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,reuest,format=None):
        user = Part_img_doc.objects.all()
        serializer = PartimgdocSendSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        user = Part_img_doc.objects.get(id=id)
        print('dgf',user)
        serializer = PartimgdocSendSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'msg':'Data update successfully',
                'data':serializer.data,
                'status':True
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self,request,id,format=None):
        try:
            user = Part_img_doc.objects.get(id=id) 
            user.delete()
            return Response({"msg":"Data delete successfully "},status=status.HTTP_201_CREATED)  
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class UpdatePartsView(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,reuest,format=None):
        user = Parts_db.objects.all()
        serializer = PratsGetSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        user = Parts_db.objects.get(id=id)
        print('dgf',user)
        serializer = PratsGetSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self,request,id,format=None):
        try:
            user = Parts_db.objects.get(id=id) 
            user.delete()
            return Response({"msg":" Part deleted successfully "},status=status.HTTP_201_CREATED)  
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

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
        serializer = PratsGetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response={
                'msg':'Parts deatails add',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTaskView(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,reuest,format=None):
        user = Task_db.objects.all()
        serializer = TaskGetSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        user = Task_db.objects.get(id=id)
        print('dgf',request.data)
        serializer = TaskaddSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        try:
            user = Task_db.objects.get(id=id) 
            user.delete()
            return Response({"msg":" Task deleted successfully "},status=status.HTTP_201_CREATED)   
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
            
class TaskView(APIView):
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAdminUser]
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

    def get(self,request, format=None):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAuthenticated]
        current_user=request.user.id
        user = Task_db.objects.filter(emp_id=current_user)
        serializer = TaskSerializer(user,many=True)
        serializer=serializer.data
        print(">>>>>>>>>>>>>",current_user)
        return Response(serializer,status=status.HTTP_201_CREATED)
    
class InventoryView(APIView): 
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAdminUser]
    def post(self, request, format=None):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response={
                'msg':'Inventory add',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,reuest,format=None):
        user = Inventory_db.objects.all()
        serializer = InventorySerializer(user,many=True)
        return Response(serializer.data,status=200)
    
    def put(self, request,id,):
        user = Inventory_db.objects.get(id=id)
        print('dgf',request.data)
        serializer = InventorySerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id,format=None):
        try:
            user = Inventory_db.objects.get(id=id) 
            user.delete()
            return Response({"msg":" Inventory deleted successfully "},status=status.HTTP_201_CREATED)   
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

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
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id,format=None):
        try:
            user = Transporter_db.objects.get(id=id) 
            user.delete()
            return Response({"msg":" Transporter deleted successfully "},status=status.HTTP_201_CREATED)   
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class LeaveapplicationView(APIView): 
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAdminUser]
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        serializer = LeaveSendSerializer(data=request.data)
        user = Leave_application_db.objects.all()
        if serializer.is_valid(raise_exception=True):
            serializer.save(emp_id_id=request.user.id)
            response={
                'msg':'Leave request sent successfully ',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,format=None):
        user = Leave_application_db.objects.all()
        obj1=Leave_application_db.objects.filter(emp_id_id=request.user.id).all()
        serializer = LeaveAdminSerializer(obj1,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        user = Leave_application_db.objects.get(id=id)
        serializer = LeaveSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id,format=None):
        try:
            user = Leave_application_db.objects.get(id=id) 
            user.delete()
            return Response({"msg":" Leave appliction deleted successfully "},status=status.HTTP_201_CREATED)   
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
# class Leaveapplicationfilter(APIView):
#     authentication_classes=[TokenAuthentication]
#     permission_classes=[IsAuthenticated]
#     def post(self,request):
#         try:
#             user =request.user
#             current_user=request.user.id
#             obj1=Leave_application_db.objects.filter(emp_id=current_user).all()
#             month=request.data.get('month')
#             all_months = []
#             if obj1:
#                 for i in obj1:
#                     leave_month = i.created_date
#                     d = str(leave_month)
#                     months=str(d[5:7])
#                     print(month)

#                     if month == months:
#                         obj = Leave_application_db.objects.filter(created_date=leave_month).all()
#                         serializer = LeaveAdminSerializer(obj,many=True)
#                         data1 =serializer.data
#                         all_months.extend(data1)
#                 return Response (all_months,status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
#         except Exception as e:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Q

class Leaveapplicationfilter(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_user = request.user.id
            obj1 = Leave_application_db.objects.filter(emp_id=current_user).all()
            month = request.data.get('month')
            all_months = []

            if obj1:
                for i in obj1:
                    leave_month = i.from_date.month  # Extract the month from the created_date
                    if str(leave_month).zfill(2) == month:  # Compare as strings, zero-padded if necessary
                        serializer = LeaveSendSerializer(i)  # Use the serializer for individual object
                        all_months.append(serializer.data)

                return Response(all_months, status=status.HTTP_201_CREATED)
            else:
                return Response(all_months, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class LeaveapplicationViewAdmin(APIView):

    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    def get(self,request,format=None):
        user = Leave_application_db.objects.all()
        serializer = LeaveAdminSerializer(user,many=True)
        return Response(serializer.data,status=200)
    
    def put(self, request,id):
        user = Leave_application_db.objects.get(id=id)
        serializer = LeaveAdminSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)

            # create_random_user_accounts.delay(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Get_UserHistory(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            user =request.user
            current_user=request.user.id
            obj1=Timesheet_db.objects.filter(emp_id=current_user).all()
            check_in = []
            check_out = []
            for i in obj1:
                check_in_time = i.check_in_time
                if check_in_time:
                    d = str(check_in_time)
                    check_in_str = datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %I:%M:%S %p')
                    check_in.append(check_in_str)
                check_out_time = i.check_out_time
                if check_out_time:
                    a = str(check_out_time)
                    check_out_str = datetime.strptime(a[:19], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %I:%M:%S %p')
                    check_out.append(check_out_str)
            return Response({'userid':f'{current_user}','check_in_time':check_in,'check_out_time':check_out},status=status.HTTP_201_CREATED)
        # return Response("done")
        except:
            return Response({'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request):
        try:
            user =request.user
            current_user=request.user.id
            obj1=Timesheet_db.objects.filter(emp_id=current_user).all()
            month=request.data.get('month')
            check_in = []
            check_out = []
            d2 = []
            for i in obj1:
                check_in_time = i.check_in_time
                check_out_time = i.check_out_time
                d = str(check_in_time)
                a = str(check_out_time)
                months=str(d[5:7])
                day_in = str(d[8:10])
                day_out = str(a[8:10])
                if month == months:
                    try:
                        data_dict = {}
                        d1 = []
                        if d!="None" and  a == "None":
                            check_in_str = datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %I:%M:%S %p')
                            check_in.append(check_in_str)
                            a = str(check_out_time)
                            check_out.append(a)
                            data_dict["check_in"] = check_in_str
                            data_dict["check_out"] = a
                            d1.append(data_dict)
                        elif d!="None" and a!="None":
                        # elif d == "None":
                        #     check_in.append(d)
                            check_in_str = datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %I:%M:%S %p')
                            check_in.append(check_in_str)
                            check_out_str = datetime.strptime(a[:19], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %I:%M:%S %p')
                            
                            check_out.append(check_out_str)
                            # data_dict[check_in_str] = a
                            data_dict["check_in"] = check_in_str
                            data_dict["check_out"] = check_out_str
                            d1.append(data_dict)
                        d2.extend(d1[0:])
                    except Exception as e:
                        print("i am else")
            sorted_list = sorted(d2, key=lambda x: (x['check_in']))
            return Response({'userid':f'{current_user}',"date":sorted_list},status=status.HTTP_201_CREATED)
        except:
            return Response({'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class TimesheetView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        current_user = request.user.id
        obj1 = Timesheet_db.objects.filter(emp_id=current_user).all()
        today = date.today()
        l1 = []  # List for check-out times
        l2 = []  # List for check-in times
        for i in obj1:
            check_in_time = i.check_in_time
            check_out_time = i.check_out_time
            if check_out_time:
                check_out_date = check_out_time.date()
                if check_out_date == today:
                    check_out_co = check_out_time.strftime('%Y-%m-%d %H:%M:%S')
                    l1.append(check_out_co)
            if check_in_time:
                check_in_date = check_in_time.date()
                if check_in_date == today:
                    check_in_ci = check_in_time.strftime('%Y-%m-%d %H:%M:%S')
                    l2.append(check_in_ci)
        return Response({'userid': current_user, 'check_in_time': l2, 'check_out_time': l1}, status=status.HTTP_201_CREATED)
        # return Response("done")
    # def post(self,request):
    #     # try:
    #             #get current user
    #     current_user=request.user.id
    #     check_in_time=request.data.get('check_in_time')
    #     check_out_time=request.data.get('check_out_time')
        
    #     #convert check-in check-out in str to datetime object
    #     if check_in_time:
    #         check_in_str = datetime.strptime(str(check_in_time), "%Y-%m-%d %H:%M:%S")
    #     else:
    #         check_in_time=None
        
    #     if check_out_time:
    #         check_out_str = datetime.strptime(str(check_out_time), "%Y-%m-%d %H:%M:%S")
    #     else:
    #         check_out_time=None
    #     if check_in_time and not check_out_time:
    #         try:
    #             time_sheet_obj=Timesheet_db.objects.filter(id=current_user).get(check_in_time__contains=check_out_str.date())

    #             if time_sheet_obj:
    #                 response={
    #                 'msg':'You Have Already Check In....',
    #                 'status':True
    #             }
    #             return Response(response)
    #         except:
    #             time_sheet=Timesheet_db(check_in_time=check_in_time)
    #     if check_out_time: 
    #         # try:
    #         time_sheet=Timesheet_db.objects.filter(id=current_user).get(check_in_time__contains=check_out_str.date())
    #         if time_sheet:
    #             #hours_for_the_day  
    #             check_in_str = datetime.strptime(str(time_sheet.check_in_time)[:19], "%Y-%m-%d %H:%M:%S")
    #             hours_difference = abs(check_in_str - check_out_str).total_seconds() / 3600.0
    #             if int(hours_difference) < 9:
    #                 response={
    #                     'msg':'Please Complete Your working Hour  ....',
    #                     'status':False
    #                 }
    #                 return Response(response,status=status.HTTP_400_BAD_REQUEST)
    #             time_sheet.check_out_time=check_out_time
    #             time_sheet.hours_for_the_day=hours_difference
    #             check_in_time=time_sheet.check_in_time
    #         # except Exception:
    #         #     response={
    #         #         'msg':'Please Check In....',
    #         #         'status':True
    #         #     }
    #         #     return Response(response,status=status.HTTP_400_BAD_REQUEST)
    #     time_sheet.save()
    #     time_sheet_obj=Timesheet_db.objects.get(id=time_sheet.id)
    #     # #add user
        # user_obj=User.objects.get(id=current_user)
        # if user_obj:
        #     time_sheet_obj.emp_id=user_obj
        
        # # #add project data of employee
        # project_obj=Project_db.objects.filter(emp__id=user_obj.id)
        # if project_obj:
        #     for i in project_obj:
        #         pr_obj=Project_db.objects.get(id=i.id)
        #         if pr_obj:
        #             time_sheet_obj.projet_id.add(pr_obj.id)
        # #add parts data of employee
        # parts_obj=Parts_db.objects.filter(emp_id__id=user_obj.id)
        # if parts_obj:
        #     for i in parts_obj:
        #         part_obj=Parts_db.objects.get(id=i.id)
        #         if part_obj:
        #             time_sheet_obj.parts_id.add(part_obj.id)
        # # add task data of employee
        # tasks_obj=Task_db.objects.filter(emp_id__id=user_obj.id)
        # if tasks_obj:
        #     for i in tasks_obj:
        #         task_obj=Task_db.objects.get(id=i.id)
        #         if task_obj:
        #             time_sheet_obj.task_id.add(task_obj.id)
        # time_sheet_obj.save()
    
    #     response={
    #         'msg':"Timesheet added Sucessfully",
    #         'check_in_time':check_in_time,
    #         'check_out_time':check_out_time,
    #         'status':True
    #     }
    #     return Response(response, status=status.HTTP_200_OK)
        # except Exception as e:
        #     response={
        #         'msg':"Something went wrong",
        #         'status':False
        #     } 
        #     # return Response(response, status=status.HTTP_400_BAD_REQUEST)
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAdminUser]
        
    def post(self, request, format=None):

        
                
        check_in_time =  request.data.get("check_in_time")
        check_out_time =  request.data.get("check_out_time")
        current_user=request.user.id
        today =date.today()
        # Leave_application = Leave_application_db.objects.filter(emp_id_id=current_user).all()
        Leave_application = Leave_application_db.objects.filter(emp_id_id=current_user, created_date__date=today).values_list('is_approved', flat=True)
        if "is_approved" == Leave_application:
            print(" ia m in")
            return Response ( {'msg':f'{user}  check out','check_out_time':check_out_st}  ,status=status.HTTP_201_CREATED)
        Leave_application_b = Leave_application_db.objects.filter(emp_id_id=current_user).values_list('created_date', flat=True)

        # is_approved = None  # assign a default value here
        # for j in Leave_application:
        #     if today == j.created_date.date():
        #         is_approved = j.is_approved
        #         print("i am ",is_approved)
        # if is_approved == "Approved":  # check if is_approved has been assigned a value
        # print("i am in",Leave_application)

        if check_in_time:
                check_in_str = datetime.strptime(str(check_in_time), "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %I:%M:%S %p')
        if check_out_time:
                check_out_st = datetime.strptime(str(check_out_time), "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %I:%M:%S %p')
        user = request.user
        hours_for_the_day = ""
        user_id=User.objects.get(id=user.id)
        obj1 = Task_db.objects.all()
        obj2 = Timesheet_db.objects.all()  
        obj=Project_db.objects.all()
        for i in obj:
            # print(i.emp.all())
            for j in  i.emp.all():
                if user == j:
                    project_id = (i.id)
                    project_obj = Project_db.objects.get(id=project_id)
        for i in obj1:
            # print(i.emp_id)
            if i.emp_id == user:
                parts_id = i.parts_id
                task_id = i.id
                task_obj = Task_db.objects.get(id =task_id )
        try:       
            if check_out_time:
                timeobj = Timesheet_db.objects.all()
                for i in timeobj:
                    if user_id == i.emp_id:
                        d = i.check_in_time
                        datetime_str = str(d)
                        d1 = datetime_str[0:10]
                        d2 = check_out_time[0:10]
                        if d1 == d2:
                            datetime_str = str(d)
                            new_dt = datetime_str[:19]
                            old_format = '%Y-%m-%d %H:%M:%S'
                            new_format = '%d-%m-%Y %H:%M:%S'
                            new_datetime_str = datetime.strptime(new_dt, old_format).strftime(new_format)
                            checkout_datetime_str = datetime.strptime(check_out_time, old_format).strftime(new_format)
                            check_in_str = datetime.strptime(new_datetime_str, "%d-%m-%Y %H:%M:%S")
                            check_out_str = datetime.strptime(checkout_datetime_str, "%d-%m-%Y %H:%M:%S")
                            hours_difference = abs(check_out_str -check_in_str).total_seconds() / 3600.0
                            Leave_application = Leave_application_db.objects.filter(emp_id_id=current_user, created_date__date=today).values_list('is_approved', flat=True)
                            # if "Approved" == str(Leave_application[0]): 
                            #     print("i am a")
                            #     return Response ( {'msg':f'{user}  check out','check_out_time':check_out_st}  ,status=status.HTTP_201_CREATED)
                            # elif "Approved" != str(Leave_application):
                            #     print("i am e",str(Leave_application[0]))

                            #     return Response ( {'msg':f'{user} Please Complete Your working Hour....'}  ,status=status.HTTP_201_CREATED)
                            print( Leave_application)

                            if hours_difference >= 9 and  not Leave_application.exists():
                                print("i am if")

                                i.check_out_time = check_out_time
                                i.hours_for_the_day = hours_difference
                                i.check_out =True
                                i.save()  
                                return Response ( {'msg':'check out','check_out_time':check_out_st}  ,status=status.HTTP_201_CREATED)
                            
                            elif hours_difference >= 9 and "Approved" != str(Leave_application[0]): 
                                print("i am elif")
                                i.check_out_time = check_out_time
                                i.hours_for_the_day = hours_difference
                                i.check_out =True
                                i.save()  
                                return Response ( {'msg':'check out','check_out_time':check_out_st}  ,status=status.HTTP_201_CREATED)
                            
                            elif hours_difference < 9 and "Approved" == str(Leave_application[0]): 
                                print("i am elif")
                                i.check_out_time = check_out_time
                                i.hours_for_the_day = hours_difference
                                i.check_out =True
                                i.save()  
                                return Response ( {'msg':'check out','check_out_time':check_out_st}  ,status=status.HTTP_201_CREATED)
                            else:
                                # for i in Leave_application:
                                return Response ( {'msg':'Please Complete Your working Hour....'}  ,status=status.HTTP_201_CREATED)
        except :

            return Response ( {'msg':'Please Complete Your working Hour....'}  ,status=status.HTTP_201_CREATED)

        try:
            if check_in_time:
                # print("i am")
                # print("check_out",check_out)
                timeobj = Timesheet_db.objects.all()
                for i in timeobj:
                    # print(i.check_in)
                    if user_id == i.emp_id:
                        d = i.check_in_time
                        datetime_str = str(d)
                        d1 = datetime_str[0:10]
                        d2 = check_in_time[0:10]
                        # print("d1 s2",d1,d2)
                        if d1 == d2:
            
                            return Response({'msg':'you are alredy check_in',},status=status.HTTP_201_CREATED)
                        else:
                            print(" not match ")
                Timesheet_db(emp_id=user_id,projet_id=project_obj,parts_id=parts_id,task_id=task_obj,hours_for_the_day=hours_for_the_day,check_in=True,check_in_time=check_in_time,check_out_time=check_out_time).save()
        except:
            timesheet = Timesheet_db(emp_id=user_id,hours_for_the_day=hours_for_the_day,check_in=True,check_in_time=check_in_time,check_out_time=check_out_time)
            timesheet.save()
            time_sheet_obj=Timesheet_db.objects.get(id=timesheet.id)
            user_obj=User.objects.get(id=current_user)
            if user_obj:
                time_sheet_obj.emp_id=user_obj
            
            # #add project data of employee
            project_obj=Project_db.objects.filter(emp__id=user_obj.id)
            if project_obj:
                for i in project_obj:
                    pr_obj=Project_db.objects.get(id=i.id)
                    if pr_obj:
                        time_sheet_obj.projet_id.add(pr_obj.id)
            #add parts data of employee
            parts_obj=Parts_db.objects.filter(emp_id__id=user_obj.id)
            if parts_obj:
                for i in parts_obj:
                    part_obj=Parts_db.objects.get(id=i.id)
                    if part_obj:
                        time_sheet_obj.parts_id.add(part_obj.id)
            # add task data of employee
            tasks_obj=Task_db.objects.filter(emp_id__id=user_obj.id)
            if tasks_obj:
                for i in tasks_obj:
                    task_obj=Task_db.objects.get(id=i.id)
                    if task_obj:
                        time_sheet_obj.task_id.add(task_obj.id)
            time_sheet_obj.save()
            return Response({'msg':'Check_in','check_in_time':check_in_str} ,status=status.HTTP_201_CREATED)
        
        return Response( {'msg':'Check_in','check_in_time':check_in_time}  ,status=status.HTTP_201_CREATED)


class GetcheckinAndcheckout(APIView):
    def get(self, request, format=None):
        queryset = Timesheet_db.objects.all()
        obj = Timesheet_db.objects.filter(check_in=True)
        for i in obj:
            print(i.emp_id)

        print(obj)
        return Response("done")
from django.db import transaction
class ProjectPartView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request, format=None):
        try:
            current_user=request.user.id
            user_obj=User.objects.get(id=current_user)
            user_db = Parts_db.objects.all()
            parts_obj=Parts_db.objects.filter(emp_id__id=user_obj.id)
            project_key = []
            part_value = []
            time_value = []
            for i in parts_obj:
                part_value.append(i.part_name)
                d =str(i.created_at)
                time_value.append(d[:19])
                f =str(i.projet_id)
                obj = Project_db.objects.filter(id=int(f))
                for i in obj:
                    project_key.append(i.project_name)
            md = dict()
            d = list(zip(project_key,zip(part_value,time_value)))
            for k,v in d:
                part_name = f"'part_name :' {v[0]}"
                time = f"'time :' {v[1]}"
                d = f'{v[0]},{v[1]}'
                md.setdefault(k, []).append(d)
            list3 = []
            for k,v in md.items():
                data = {}
                if k:
                    data["project_name"]=k
                if v:
                    data["part_name"]=v
                list3.append(data)
            serializer = GetPartSerializer(user_db,many=True)
            serializer=serializer.data
            if list3:
                return Response(list3,status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'You have no projects or parts assigned.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        try:
            authentication_classes=[TokenAuthentication]
            permission_classes=[IsAuthenticated]
            project_name=request.data.get('project_name')
            part_name=request.data.get('parts_name')
            part_description = request.data.get('part_description')
            working_status = request.data.get('working_status')
            updated_at =request.data.get('updated_at')
            current_user=request.user.id
            user_obj=User.objects.get(id=current_user)
            user_db = Parts_db.objects.all()
            project = Project_db.objects.get(project_name=project_name)
            print(project_name,part_name,user_obj,">>>>>>>>>>>>")
            parts_obj=Parts_db.objects.filter(emp_id__id=user_obj.id,projet_id_id=project,part_name=part_name)
            update_time = datetime.strptime(str(updated_at), "%Y-%m-%d %H:%M:%S")
            old_format = '%Y-%m-%d %H:%M:%S'
            new_format = '%d-%m-%Y %H:%M:%S'
            for i in parts_obj:
                i.part_description = part_description
                i.working_status =working_status
                i.updated_at = updated_at
                create = str(i.created_at)
                update_datetime_str = datetime.strptime(updated_at, old_format).strftime(new_format)
                update_out_str = datetime.strptime(update_datetime_str, "%d-%m-%Y %H:%M:%S")
                new_datetime_str = datetime.strptime(create[:19], old_format).strftime(new_format)
                check_in_str = datetime.strptime(new_datetime_str, "%d-%m-%Y %H:%M:%S")
                hours_difference = abs(update_out_str -check_in_str).total_seconds() / 3600.0
                i.total_hours = hours_difference
                i.save()
            return Response({'msg':" Your task update successfully"},status=status.HTTP_201_CREATED)
        except:
            return Response({'msg':'Please check project or part name'},status=status.HTTP_400_BAD_REQUEST)
class UserUpdateApi(APIView):

    def get(self,request,format=None):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAdminUser]
        user = UserUpdate_db.objects.all()
        serializer = UserUpdate_dbSerializer(user,many=True)
        return Response(serializer.data,status=200)

    # def post(self, request):
    #     try:
    #         current_user = request.user.id
    #         project_name = request.data.get('project_name')
    #         part_name = request.data.get('parts_name')
    #         task_name = request.data.get('task_name')
    #         part_description = request.data.get('part_description')
    #         working_status = request.data.get('working_status')
    #         updated_at = request.data.get('updated_at')

    #         user_obj = User.objects.get(id=current_user)
    #         project = Project_db.objects.filter(project_name=project_name).first()
    #         part = Parts_db.objects.get(part_name=part_name)
    #         task = Task_db.objects.get(opretions=task_name)

    #         with transaction.atomic():
    #             query = UserUpdate_db.objects.filter(emp_id=current_user).exists()

    #             if query:
    #                 Task_db.objects.filter(opretions=task_name).update(working_status=working_status)
    #                 obj = UserUpdate_db.objects.all()

    #                 for i in obj:
    #                     create = str(i.created_at)
    #                     update_datetime_str = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S").strftime(
    #                         "%d-%m-%Y %H:%M:%S"
    #                     )
    #                     update_out_str = datetime.strptime(update_datetime_str, "%d-%m-%Y %H:%M:%S")
    #                     new_datetime_str = datetime.strptime(create[:19], "%Y-%m-%d %H:%M:%S").strftime(
    #                         "%d-%m-%Y %H:%M:%S"
    #                     )
    #                     check_in_str = datetime.strptime(new_datetime_str, "%d-%m-%Y %H:%M:%S")
    #                     hours_difference = abs(update_out_str - check_in_str).total_seconds() / 3600.0
    #                     i.total_hours = hours_difference

    #                     if working_status == "Complete":
    #                         Task_db.objects.filter(opretions=task_name).update(
    #                             working_status=working_status, is_updated=True
    #                         )
    #                     else:
    #                         Task_db.objects.filter(opretions=task_name).update(
    #                             working_status=working_status, is_updated=False
    #                         )
    #             else:
    #                 if working_status == "Complete":
    #                     Task_db.objects.filter(opretions=task_name).update(
    #                         working_status=working_status, is_updated=True
    #                     )
    #                 else:
    #                     Task_db.objects.filter(opretions=task_name).update(
    #                         working_status=working_status, is_updated=False
    #                     )

    #                 user_update = UserUpdate_db(
    #                     emp_id=user_obj,
    #                     projet_name=project,
    #                     part_name=part,
    #                     task_name=task,
    #                     working_status=working_status,
    #                     part_description=part_description,
    #                     updated_at=updated_at,
    #                 )
    #                 user_update.save()

    #                 # Create a new entry in UserUpdate_db for the new project or part
    #                 if project_name != user_update.projet_name.project_name:
    #                     new_project = Project_db.objects.filter(project_name=project_name).first()
    #                     new_user_update_project = UserUpdate_db(
    #                         emp_id=user_obj,
    #                         projet_name=new_project,
    #                         part_name=user_update.part_name,
    #                         task_name=user_update.task_name,
    #                         working_status=user_update.working_status,
    #                         part_description=user_update.part_description,
    #                         updated_at=user_update.updated_at,
    #                     )
    #                     new_user_update_project.save()

    #                 if part_name != user_update.part_name.part_name:
    #                     new_part = Parts_db.objects.get(part_name=part_name)
    #                     new_user_update_part = UserUpdate_db(
    #                         emp_id=user_obj,
    #                         projet_name=user_update.projet_name,
    #                         part_name=new_part,
    #                         task_name=user_update.task_name,
    #                         working_status=user_update.working_status,
    #                         part_description=user_update.part_description,
    #                         updated_at=user_update.updated_at,
    #                     )
    #                     new_user_update_part.save()

    #         return Response({'msg': "Your task has been updated successfully"}, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response({'msg': 'Please check project or part name', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        current_user=request.user.id

        # try:
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAuthenticated]
        project_name=request.data.get('project_name')
        part_name=request.data.get('parts_name')
        task_name = request.data.get('task_name')
        part_description = request.data.get('part_description')
        working_status = request.data.get('working_status')
        start_time =request.data.get('start_time')
        end_time =request.data.get('end_time')
        task_img = request.data.get('task_img')
        current_user=request.user.id
        user_obj=User.objects.get(id=current_user)
        user_db = Parts_db.objects.all()
        print(project_name,part_name,user_obj,">>>>>>>>>>>>")
        project = Project_db.objects.filter(project_name=project_name).first() 
        print("@@@@@@@@@@@@@@@",project)           
        part = Parts_db.objects.get(part_name=part_name)
        task = Task_db.objects.get(opretions=task_name)
        query=UserUpdate_db.objects.filter(emp_id=current_user,task_name_id=task.id).exists()
        old_format = '%Y-%m-%d %H:%M:%S'
        new_format = '%d-%m-%Y %H:%M:%S'
        if query:
            Task_db.objects.filter(opretions=task_name).update(working_status=working_status)
            obj = UserUpdate_db.objects.all()
            for i in obj:
                print(i.start_time)
                create = str(i.start_time)
                update_datetime_str = datetime.strptime(end_time, old_format).strftime(new_format)
                update_out_str = datetime.strptime(update_datetime_str, "%d-%m-%Y %H:%M:%S")
                new_datetime_str = datetime.strptime(create[:19], old_format).strftime(new_format)
                check_in_str = datetime.strptime(new_datetime_str, "%d-%m-%Y %H:%M:%S")
                hours_difference = abs(update_out_str -check_in_str).total_seconds() / 3600.0
                print("?????",hours_difference)
                i.total_hours = hours_difference
                i.end_time = end_time
                i.task_img = task_img
                i.save()
            if working_status == "Complete":
                Task_db.objects.filter(opretions=task_name).update(working_status=working_status,is_updated=True)
                # UserUpdate_db(emp_id=user_obj,projet_name=project,part_name=part,task_name=task,working_status=working_status,part_description=part_description,end_time=end_time).save()
            else:
                Task_db.objects.filter(opretions=task_name).update(working_status=working_status,is_updated=False)
                # UserUpdate_db(emp_id=user_obj,projet_name=project,part_name=part,task_name=task,working_status=working_status,part_description=part_description,end_time=end_time).save()
        else:
            if working_status == "Complete":
                Task_db.objects.filter(opretions=task_name).update(working_status=working_status,is_updated=True)
                UserUpdate_db(emp_id=user_obj,projet_name=project,part_name=part,task_name=task,working_status=working_status,part_description=part_description,end_time=end_time).save()

            else:
                Task_db.objects.filter(opretions=task_name).update(working_status=working_status,is_updated=False)
                UserUpdate_db(emp_id=user_obj,projet_name=project,part_name=part,task_name=task,working_status=working_status,part_description=part_description,start_time=start_time).save()

        return Response({'msg':" Your task update successfully"},status=status.HTTP_201_CREATED)
        # except:
        #     return Response({'msg':'Please check project or part name'},status=status.HTTP_400_BAD_REQUEST)

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
        


def generate_pdf(request):
    # Get the data from the Inventory_db table
    inventory_data = Inventory_db.objects.all().values_list(
        'inventory_name', 'supplier_name', 'supplier_address',
        'supplier_contact', 'stock_quantity', 'costing', 'is_available'
    )

    # Create a temporary file to save the PDF
    temp_file = NamedTemporaryFile(delete=True)

    # Create the PDF document with landscape orientation and increased height
    doc = SimpleDocTemplate(temp_file.name, pagesize=landscape(letter), bottomMargin=30)

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.30, colors.black),
    ])

    # Create a Story for the PDF content
    story = []

    # Add title
    title = Paragraph("Inventory Details", title_style)
    story.append(title)
    story.append(Paragraph("<br/><br/>", styles['Normal']))  # Add space

    # Create a table and add data to it
    table_data = [['Inventory Name', 'Supplier Name', 'Supplier Address',
                   'Supplier Contact', 'Stock Quantity', 'Costing', 'Is Available']]
       # Format the date values
    formatted_data = []
    for item in inventory_data:
        formatted_item = list(item)
        # formatted_item[-2] = item[-2].date().strftime('%Y-%m-%d')  # Format created_at
        # formatted_item[-1] = item[-1].date().strftime('%Y-%m-%d')  # Format updated_at
        formatted_data.append(formatted_item)
    
    table_data.extend(formatted_data)

    table = LongTable(table_data)
    table.setStyle(table_style)

    story.append(table)

    # Build the document
    doc.build(story)

    # Seek to the beginning of the temporary file
    temp_file.seek(0)

    # # Create a response with the temporary file content
    # response = HttpResponse(temp_file.read(), content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="purchase_order.pdf"'

    # # Close the temporary file
    # temp_file.close()
    # Create the PDF document with landscape orientation and increased height
    doc = SimpleDocTemplate(temp_file.name, pagesize=landscape(letter), bottomMargin=30)

    # Rest of the code...

    # Generate a unique filename for the PDF
    filename = "Inventory Details.pdf"

    # Save the temporary file to a permanent location
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb') as file:
        file.write(temp_file.read())

    # Create the download URL for the PDF
    download_url = reverse('download_pdf', kwargs={'filename': filename})

    # Create the response with the download URL
    response_data = {'url': download_url}
    response = JsonResponse(response_data, status=200)

    # Close the temporary file
    temp_file.close()
    return response

def project_pdf(request):
    # Get the data from the Inventory_db table
    inventory_data = Project_db.objects.all().values_list(
        'project_name', 'project_pricing', 'working_status',
        'project_description'
    )

    # Create a temporary file to save the PDF
    temp_file = NamedTemporaryFile(delete=True)

    # Create the PDF document with landscape orientation and increased height
    doc = SimpleDocTemplate(temp_file.name, pagesize=landscape(letter), bottomMargin=30)

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.30, colors.black),
    ])

    # Create a Story for the PDF content
    story = []

    # Add title
    title = Paragraph("Project Details", title_style)
    story.append(title)
    story.append(Paragraph("<br/><br/>", styles['Normal']))  # Add space

    # Create a table and add data to it
    table_data = [['Project Name', 'Project Pricing', 'Working Status',
                   'Project Description']]
       # Format the date values
    formatted_data = []
    for item in inventory_data:
        formatted_item = list(item)
        # formatted_item[-2] = item[-2].date().strftime('%Y-%m-%d')  # Format created_at
        # formatted_item[-1] = item[-1].date().strftime('%Y-%m-%d')  # Format updated_at
        formatted_data.append(formatted_item)
    
    table_data.extend(formatted_data)

    table = LongTable(table_data)
    table.setStyle(table_style)

    story.append(table)

    # Build the document
    doc.build(story)
    temp_file.seek(0)

    # Seek to the beginning of the temporary file

    # # Create a response with the temporary file content
    # response = HttpResponse(temp_file.read(), content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="Project Details.pdf"'

    # # Close the temporary file
    # temp_file.close()
    # Create a temporary file to save the PDF
    # Create a temporary file to save the PDF
    # temp_file = NamedTemporaryFile(delete=True)

    # Create the PDF document with landscape orientation and increased height
    doc = SimpleDocTemplate(temp_file.name, pagesize=landscape(letter), bottomMargin=30)

    # Rest of the code...

    # Generate a unique filename for the PDF
    filename = "Project_Details.pdf"

    # Save the temporary file to a permanent location
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb') as file:
        file.write(temp_file.read())

    # Create the download URL for the PDF
    download_url = reverse('download_pdf', kwargs={'filename': filename})

    # Create the response with the download URL
    response_data = {'url': download_url}
    response = JsonResponse(response_data, status=200)

    # Close the temporary file
    temp_file.close()
    return response



def employee_pdf(request):
    # Get the data from the User table
    inventory_data = User.objects.all().values_list(
        'full_name', 'username', 'email',
        'phone_number', 'address'
    )

    # Create a temporary file to save the PDF
    temp_file = NamedTemporaryFile(delete=True)

    # Create the PDF document with landscape orientation and increased height
    doc = SimpleDocTemplate(temp_file.name, pagesize=landscape(letter), bottomMargin=30)

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.30, colors.black),
    ])

    # Create a Story for the PDF content
    story = []

    # Add title
    title = Paragraph("Employee Details", title_style)
    story.append(title)
    story.append(Paragraph("<br/><br/>", styles['Normal']))  # Add space

    # Create a table and add data to it
    table_data = [['Full Name', 'Username', 'Email',
                   'Phone Number', 'Address']]
    table_data.extend(inventory_data)

    table = LongTable(table_data)
    table.setStyle(table_style)

    story.append(table)

    # Build the document
    doc.build(story)

    # Seek to the beginning of the temporary file
    temp_file.seek(0)

    # Generate a unique filename for the PDF
    filename = "Employee_Details.pdf"

    # Save the temporary file to a permanent location
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb') as file:
        file.write(temp_file.read())

    # Create the download URL for the PDF
    download_url = reverse('download_pdf', kwargs={'filename': filename})

    # Create the response with the download URL
    # response = HttpResponse()
    # response.write({"url":download_url})

    # response.write('<a href="{}" download>Download PDF</a>'.format(download_url))
    # response = ({"url":download_url})
    response_data = {'url': download_url}
      # Remove the file from mediafiles after the response is sent
    # def remove_file(response):
    #     os.remove(file_path)
    #     return response
    response = JsonResponse(response_data, status=200)
    return response

def download_pdf(request, filename):
    # Get the file path
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Create a response with file content as attachment
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    return response


def calculate_gst_and_total(costing):
    gst_percentage = 18
    numeric_costing = re.findall(r'\d+\.?\d*', costing)
    if not numeric_costing:
        raise ValueError("Invalid costing value")
    costing_value = float(numeric_costing[0])
    gst_amount = (gst_percentage / 100) * costing_value
    total_amount = costing_value + gst_amount
    gst_amount = round(gst_amount, 2)
    total_amount = round(total_amount, 2)

    return gst_amount, total_amount

class generate_purchase_order_bills(APIView):
    def post(self,request):
        shop_name = request.data.get('shop_name')
        account_details = request.data.get('account_details')
        inventory_names = request.data.get('inventory_names', [])

        temp_file = NamedTemporaryFile(delete=True)
        # Create the PDF document with landscape orientation and increased height
        doc = SimpleDocTemplate(temp_file.name, pagesize=landscape(letter), bottomMargin=30)

        # Set up styles
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']

        # Define table styles
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Create a Story for the PDF content
        story = []

        # Add shop name and account details
        story.append(Paragraph("Shop Name: {}".format(shop_name), styles['Normal']))
        story.append(Paragraph("Account Details: {}".format(account_details), styles['Normal']))
        story.append(Paragraph("<br/><br/>", styles['Normal']))

        # Loop through each inventory name and generate purchase order bill
        for inventory_name in inventory_names:
            inventory_data = Inventory_db.objects.filter(inventory_name=inventory_name).values_list(
                'inventory_name', 'supplier_name', 'supplier_address',
                'supplier_contact', 'stock_quantity', 'costing'
            ).first()

            if not inventory_data:
                print("Inventory name not found:", inventory_name)
                continue

            # Generate purchase order bill for the current inventory name
            inventory_name, supplier_name, supplier_address, supplier_contact, stock_quantity, costing = inventory_data

            # Calculate GST and total amount
            gst_amount, total_amount = calculate_gst_and_total(costing)

            # Add title
            title = Paragraph("Purchase Order - {}".format(inventory_name), title_style)
            story.append(title)
            story.append(Paragraph("<br/><br/>", styles['Normal']))

            # Create a table and add data to it
            table_data = [
                ['Inventory Name', 'HSN', 'Supplier Name', 'Supplier Address', 'Supplier Contact',
                'Stock Quantity', 'Costing', 'GST', 'Total Amount'],
                [inventory_name, '8466', supplier_name, supplier_address, supplier_contact,
                stock_quantity, costing, gst_amount, total_amount]
            ]

            table = Table(table_data)
            table.setStyle(table_style)

            story.append(table)
            story.append(Paragraph("<br/><br/>", styles['Normal']))

        # Build the document
        doc.build(story)
        temp_file.seek(0)

        print("Purchase order bills generated successfully")

        # Generate a unique filename for the PDF
        filename = "purchase_orders.pdf"

        # Save the temporary file to a permanent location
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        with open(file_path, 'wb') as file:
            file.write(temp_file.read())

        # Create the download URL for the PDF
        download_url = reverse('download_pdf', kwargs={'filename': filename})

        # Create the response with the download URL
        response_data = {'url': download_url}
        response = JsonResponse(response_data, status=200)

        # Close the temporary file
        temp_file.close()
        return response

class projectdata_pdf(APIView):
    def post(self, request):
        # Get the project names from the request data
        project_names = request.data.get('project_name', [])
        # Retrieve the data for each project name
        inventory_data = []
        for project_name in project_names:
            project_data = Project_db.objects.filter(project_name=project_name).values_list(
                'project_name', 'project_pricing', 'working_status', 'project_description'
            )
            inventory_data.extend(project_data)
        # Create a temporary file to save the PDF
        temp_file = NamedTemporaryFile(delete=True)

        # Create the PDF document with landscape orientation and increased height
        doc = SimpleDocTemplate(temp_file.name, pagesize=landscape(letter), bottomMargin=30)

        # Set up styles
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        table_style = TableStyle([
            # Table style definitions...
        ])

        # Create a Story for the PDF content
        story = []

        # Add title
        title = Paragraph("Project Details", title_style)
        story.append(title)
        story.append(Paragraph("<br/><br/>", styles['Normal']))  # Add space

        # Create a table and add data to it
        table_data = [['Project Name', 'Project Pricing', 'Working Status', 'Project Description']]

        # Format the date values
        formatted_data = []
        for item in inventory_data:
            formatted_item = list(item)
            # formatted_item[-2] = item[-2].date().strftime('%Y-%m-%d')  # Format created_at
            # formatted_item[-1] = item[-1].date().strftime('%Y-%m-%d')  # Format updated_at
            formatted_data.append(formatted_item)

        table_data.extend(formatted_data)

        table = LongTable(table_data, repeatRows=1)
        table.setStyle(table_style)

        story.append(table)

        # Build the document
        doc.build(story)
        temp_file.seek(0)

        # Generate a unique filename for the PDF
        filename = "Projects.pdf"

        # Save the temporary file to a permanent location
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        with open(file_path, 'wb') as file:
            file.write(temp_file.read())

        # Create the download URL for the PDF
        download_url = reverse('download_pdf', kwargs={'filename': filename})

        # Create the response with the download URL
        response_data = {'url': download_url}
        response = JsonResponse(response_data, status=200)

        # Close the temporary file
        temp_file.close()

        return response


#Gwt api for all withi pagination -------------------    
class Getusers(ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserGetAll
    pagination_class = CustomPagination

class Getproject(ListAPIView):
    # def get(self,request, format=None):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = Project_db.objects.all()
    serializer_class = ProjectGetallSerializer
    pagination_class = CustomPagination

    # serializer=serializer.data
    # return Response(serializer, status=status.HTTP_201_CREATED)

    # def get_serializer_class(request):
    #     user = request.user
    #     print("******************",user)
    #     if user.is_superuser:
    #         # Return a serializer class that includes all fields
    #         return ProjectGetallSerializer

    #     # Return a serializer class that excludes specific fields
    #     class CustomSerializer(PratsGetSerializer):
    #         class Meta:
    #             model = Project_db
    #             exclude = ['id', 'project_name','working_status', 'project_description', 'project_inventory', 'created_at', 'emp', 'inventory']  # Specify the fields you want to exclude

    #     return CustomSerializer

class Getpart(ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = Parts_db.objects.all()
    serializer_class = PartImgDocSerializer
    pagination_class = CustomPagination

class Gettask(ListAPIView):
    # def get(self,reuest,format=None):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = Task_db.objects.all()
    serializer_class = TaskallSerializer
    pagination_class = CustomPagination

    # user = Task_db.objects.all()
    # serializer = TaskallSerializer(user,many=True)
    # return Response(serializer.data,status=status.HTTP_201_CREATED)

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
    serializer_class = ProjectGetSerializer
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