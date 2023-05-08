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

# Create your views here.



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

   
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        username = request.data['username']
        password= request.data['password']
        if serializer.is_valid():
            user=serializer.save()
            authenticate(username=username, password=password)
            login(request,user)
            token = Token.objects.get_or_create(user=user)[0].key
            # resfresh = RefreshToken.for_user(user)
            # response_data = {'refresh':str(resfresh),'access':str(resfresh.access_token), "token": AuthToken.objects.create(user)[1]}
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
        print('dgf',id)
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


# class UserLoginView(APIView):
#     """ 
#         Login User....
#     """
#     def post(self, request, format=None):
#         obj =  User.objects.all()
#         # for j in obj:
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             username = serializer.data.get('username')
#             password = serializer.data.get('password')
#             user_username=User.objects.filter(username=username).first()
#             if user_username:
#                     user_username.is_active=True
#                     user_username.save()
#                     user = authenticate(username=username, password=password)
#                     # User.is_active = True
#                     # token = get_tokens_for_user(j)
#                     token = Token.objects.get_or_create(user=user)[0].key
#                     if user :
#                         response={
#                                 'token':token,
#                                 'msg':'Login Success',
#                                 'status':True,
#                                 'username':username
#                             }
#                         return Response(response, status=status.HTTP_201_CREATED)
                    
#                     # else:
#                     #     return Response({'errors':{'non_field_errors':['name or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
#             elif user_username==None:
#                     response={
#                                 'msg':f' Please Add valid Username {username}',
#                                 'status':False,
                                
#                             }
#                 # Response("Something went wrong",sstatus=status.HTTP_400_BAD_REQUEST)

#                     return Response(response,status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
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

                print("~~~~~~~~~~~", user_)
                # User.is_active = True
               

                if user_:
                    token = Token.objects.get_or_create(user=user)[0].key
                    response={
                                'token':token,
                                'msg':'Login Success',
                                'status':True,
                                'username':username
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
    def get(self,reuest,format=None):
        user = Project_db.objects.all()
        serializer = ProjectGetSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class UpdateProjects(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,reuest,format=None):
        user = Project_db.objects.all()
        serializer = ProjectGetSerializer(user,many=True)
        return Response({"msg":serializer.data},status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        # id = request.data.get('check_in')

        user = Project_db.objects.get(id=id)
        print('dgf',id)
        serializer = ProjectSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # return Response("Project updated successfully ")
    
    def delete(self,request,id,format=None):
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
    

class UpdatePartsView(APIView): 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,reuest,format=None):
        user = Parts_db.objects.all()
        serializer = PratsGetSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self, request,id,):
        user = Parts_db.objects.get(id=id)
        print('dgf',request.data)
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
        serializer = PartSerializer(data=request.data)
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
        serializer = TaskGetSerializer(user, data=request.data)
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
       
        serializer = TaskSerializer(data=request.data)
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
        serializer = TaskGetSerializer(user,many=True)
        serializer=serializer.data
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
class Leaveapplicationfilter(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            user =request.user
            current_user=request.user.id
            obj1=Leave_application_db.objects.filter(emp_id=current_user).all()
            month=request.data.get('month')
            all_months = []
            if obj1:
                for i in obj1:
                    leave_month = i.created_date
                    d = str(leave_month)
                    months=str(d[5:7])
                    if month == months:
                        obj = Leave_application_db.objects.filter(created_date=leave_month).all()
                        serializer = LeaveAdminSerializer(obj,many=True)
                        data1 =serializer.data
                        all_months.extend(data1)
                return Response (all_months,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
        except Exception as e:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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
                            # print(day_in,day_out,"@@@@@@@@@@@@@@")
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
    
    def get(self,request):
        current_user=request.user.id
        obj1=Timesheet_db.objects.filter(emp_id=current_user).all()
        today = datetime.today().date()
        todays = str(today) 
        l1 = []
        l2 = []
        for i in obj1:
            check_in_time = i.check_in_time
            check_out_time = i.check_out_time
            if check_out_time:
                check_out = str(check_out_time.date())
                try:
                    if todays == check_out:
                        check_out_co = str(check_out_time)[:19]
                        l1.append(check_out_co)
                except Exception as e:
                    return Response(e,status=status.HTTP_400_BAD_REQUEST)
            if check_in_time:
                check_in = str(check_in_time.date())
                try:
                    if todays == check_in:
                        check_in_ci = str(check_in_time)[:19]
                        l2.append(check_in_ci)
                        print(check_in_ci)
                except Exception as e:
                    return Response(e,status=status.HTTP_400_BAD_REQUEST)
        return Response({'userid':f'{current_user}','check_in_time':l2,'check_out_time':l1},status=status.HTTP_201_CREATED)
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
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
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
        print("user_______",user)
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
                                return Response ( {'msg':f'{user}  check out','check_out_time':check_out_st}  ,status=status.HTTP_201_CREATED)
                            
                            elif hours_difference >= 9 and "Approved" != str(Leave_application[0]): 
                                print("i am elif")
                                i.check_out_time = check_out_time
                                i.hours_for_the_day = hours_difference
                                i.check_out =True
                                i.save()  
                                return Response ( {'msg':f'{user}  check out','check_out_time':check_out_st}  ,status=status.HTTP_201_CREATED)
                            
                            elif hours_difference < 9 and "Approved" == str(Leave_application[0]): 
                                print("i am elif")
                                i.check_out_time = check_out_time
                                i.hours_for_the_day = hours_difference
                                i.check_out =True
                                i.save()  
                                return Response ( {'msg':f'{user}  check out','check_out_time':check_out_st}  ,status=status.HTTP_201_CREATED)
                            else:
                                # for i in Leave_application:
                                print("~~~~~~~~>>",str(Leave_application[0]))
                                return Response ( {'msg':f'{user} Please Complete Your working Hour....'}  ,status=status.HTTP_201_CREATED)
        except :

            return Response ( {'msg':f'{user} Please Complete Your working Hour....'}  ,status=status.HTTP_201_CREATED)

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
            return Response({'msg':f'{user} Check_in','check_in_time':check_in_str} ,status=status.HTTP_201_CREATED)
        
        return Response( {'msg':f'{user} Check_in','check_in_time':check_in_time}  ,status=status.HTTP_201_CREATED)


class GetcheckinAndcheckout(APIView):
    def get(self, request, format=None):
        queryset = Timesheet_db.objects.all()
        obj = Timesheet_db.objects.filter(check_in=True)
        for i in obj:
            print(i.emp_id)

        print(obj)
        return Response("done")

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
    def post(self,request):
        current_user=request.user.id

        print(current_user,"?????")
        try:
            authentication_classes=[TokenAuthentication]
            permission_classes=[IsAuthenticated]
            project_name=request.data.get('project_name')
            part_name=request.data.get('parts_name')
            task_name = request.data.get('task_name')
            part_description = request.data.get('part_description')
            working_status = request.data.get('working_status')
            updated_at =request.data.get('updated_at')
            current_user=request.user.id
            user_obj=User.objects.get(id=current_user)
            user_db = Parts_db.objects.all()
            # print("project",project_name)
            project = Project_db.objects.get(project_name=project_name)
            # print(project)
            part = Parts_db.objects.get(part_name=part_name)
            # print(str(part))

            task = Task_db.objects.get(opretions=task_name)
            # print(task,"i am task")
            query=UserUpdate_db.objects.filter(emp_id=current_user).exists()
            old_format = '%Y-%m-%d %H:%M:%S'
            new_format = '%d-%m-%Y %H:%M:%S'
            if query:
                Task_db.objects.filter(opretions=task_name).update(working_status=working_status)
                # UserUpdate_db.objects.filter(projet_name_id=project).update(total_hours=1)
                obj = UserUpdate_db.objects.all()
                for i in obj:
                    print(i.created_at)
                    create = str(i.created_at)
                    update_datetime_str = datetime.strptime(updated_at, old_format).strftime(new_format)
                    update_out_str = datetime.strptime(update_datetime_str, "%d-%m-%Y %H:%M:%S")
                    new_datetime_str = datetime.strptime(create[:19], old_format).strftime(new_format)
                    check_in_str = datetime.strptime(new_datetime_str, "%d-%m-%Y %H:%M:%S")
                    hours_difference = abs(update_out_str -check_in_str).total_seconds() / 3600.0
                    i.total_hours = hours_difference
                    if working_status == "completed":
                        Task_db.objects.filter(opretions=task_name).update(working_status=working_status,is_updated=True)
                    else:
                        Task_db.objects.filter(opretions=task_name).update(working_status=working_status,is_updated=False)
            else:
                if working_status == "completed":
                    Task_db.objects.filter(opretions=task_name).update(working_status=working_status,is_updated=True)
                else:
                    Task_db.objects.filter(opretions=task_name).update(working_status=working_status,is_updated=False)
                obj = UserUpdate_db(emp_id=user_obj,projet_name=project,part_name=part,task_name=task,working_status=working_status,part_description=part_description,updated_at=updated_at).save()

            return Response({'msg':" Your task update successfully"},status=status.HTTP_201_CREATED)
        except:
            return Response({'msg':'Please check project or part name'},status=status.HTTP_400_BAD_REQUEST)
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
        
#Gwt api for all withi pagination -------------------    
class Getusers(ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserGetAll
    pagination_class = CustomPagination

class Getproject(APIView):
    def get(self,request, format=None):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAuthenticated]
        user = Project_db.objects.all()
        serializer = ProjectGetSerializer(user,many=True)
        serializer=serializer.data
        return Response(serializer, status=status.HTTP_201_CREATED)

class Getpart(ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    queryset = Parts_db.objects.all()
    serializer_class = PratsGetSerializer
    pagination_class = CustomPagination

class Gettask(APIView):
    def get(self,reuest,format=None):
        user = Task_db.objects.all()
        serializer = TaskSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

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