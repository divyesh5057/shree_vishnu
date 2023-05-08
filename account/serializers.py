from rest_framework import serializers
from account.models import * #User,Project_db,Parts_db,Task_db,Timesheet_db
from datetime import datetime



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password is not same")
        
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserGetAll(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['id','username','email']

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'password']



class UserlogoutSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username']

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project_db
        fields = '__all__'

class GetInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory_db
        fields = ['inventory_name']
class ProjectGetSerializer(serializers.ModelSerializer):
    inventory = GetInventorySerializer(many=True,read_only=True)    
    working_status = serializers.SerializerMethodField() 
    emp = UserlogoutSerializer(many=True,read_only=True) 
    def get_working_status(self,request,*args):
        current_user=request
        user = Project_db.objects.filter(id=str(current_user))
        # print(user,">>>>")
        # obj = Project_db.objects.filter(emp= str(request.emp))
        for i in user:
            data = (i.working_status)
            # data.capitalize()
            # print((data.capitalize()),"~~~~~~~~~~>>>>")
        return data.capitalize()
    class Meta:
        model = Project_db
        fields = ['id','project_name','project_pricing','working_status','project_description','project_inventory','created_at','emp','inventory']

class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parts_db
        fields = '__all__'

class PratsGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parts_db
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task_db
        fields = ['id','parts_quantity','opretions','working_status','created_date','updated_date','emp_id','projet_id','parts_id']

class TaskGetSerializer(serializers.ModelSerializer):
    working_status = serializers.SerializerMethodField() 
    projet_id = serializers.SerializerMethodField() 
    parts_id = serializers.SerializerMethodField() 


    def get_working_status(self,request,*args):
        current_user=request
        user = Task_db.objects.filter(id=str(current_user))
        # print(user,">>>>")
        # obj = Project_db.objects.filter(emp= str(request.emp))
        for i in user:
            data = (i.working_status)
            # data.capitalize()
            # print((data.capitalize()),"~~~~~~~~~~>>>>")
        return data.capitalize()
    
    def get_projet_id(self,request,*args):
        current_user=request
        # print(*args,">>>>>>>>>>")
        user = Task_db.objects.filter(id=str(current_user))
        
        for i in user:
            data = (i.projet_id)
            project = Project_db.objects.filter(id=str(data))
            for j in project:
                pass
        return j.project_name
    
    def get_parts_id(self,request,*args):
        current_user=request
        # print(*args,">>>>>>>>>>")
        user = Task_db.objects.filter(id=str(current_user))
        
        for i in user:
            data = (i.parts_id)
            project = Parts_db.objects.filter(id=str(data))
            for j in project:
                pass
        return j.part_name
    class Meta:
        model = Task_db
        fields = ['id','emp_id','parts_quantity','opretions','working_status','created_date','updated_date','projet_id','parts_id','is_updated']
class TimesheetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Timesheet_db
        # fields=['check_in_time','check_out_time']
        fields = ['emp_id','projet_id','parts_id','task_id','hours_for_the_day','check_in','check_out',]

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory_db
        fields = '__all__'

class TransporterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transporter_db
        fields = '__all__'


class GetProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_db
        fields = ['project_name']

class GetPartSerializer(serializers.ModelSerializer):
    # projet_id = serializers.SerializerMethodField()

    class Meta:
        model = Parts_db
        fields = ['id','projet_id','part_name','working_status','part_description','updated_at']
class GetProjectParts(serializers.ModelSerializer):
    parts_id = GetPartSerializer(many=True,read_only=True)    
    # projet_id = GetProjectSerializer(many=True,read_only=True)
    class Meta:
        model = Timesheet_db
        fields = ['id','projet_id','parts_id','part_description','working_status','updated_at']

class LeaveSerializer(serializers.ModelSerializer):
    from_date = serializers.SerializerMethodField()
    to_date = serializers.SerializerMethodField()
    is_approved = serializers.SerializerMethodField()


    def get_from_date(self,request,*args):
        obj = Leave_application_db.objects.filter(emp_id_id= str(request.emp_id))
        for i in obj:
            date = (i.from_date)
            d = str(date)
        if d:
            # print(d,">>>>>")
            date1 = datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %I:%M:%S %p')
            # print(">>>>>>>>>>",date1)
        return date1
    
    def get_to_date(self,request,*args):
        obj = Leave_application_db.objects.filter(emp_id_id= str(request.emp_id))
        for i in obj:
            date = (i.to_date)
            d = str(date)
        if d:
            date1 = datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %I:%M:%S %p')
        return date1
    
    def get_is_approved(self,request,*args):
        obj = Leave_application_db.objects.filter(emp_id_id= str(request.emp_id))
        for i in obj:
            data = (i.is_approved)
            data.capitalize()
            # print(date,"~~~~~~~~~~>>>>")
        return data

    class Meta:
        model = Leave_application_db
        fields = ['id','from_date','to_date','leave_type','total_leave','leave_application','created_date','is_approved']

class LeaveSendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leave_application_db
        fields = '__all__'

class LeaveAdminSerializer(serializers.ModelSerializer):
    emp_id = serializers.SerializerMethodField()
    from_date = serializers.SerializerMethodField()
    to_date = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    def get_emp_id(self,request,*args):
        obj = User.objects.get(pk= str(request.emp_id))
        return obj.username
    
    def get_from_date(self,request,*args):
        obj = Leave_application_db.objects.filter(emp_id_id= str(request.emp_id))
        for i in obj:
            date = (i.from_date)
            d = str(date)
        if d:
            # print(d,">>>>>")
            date1 = datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S")
            # print(">>>>>>>>>>",date1)
        return date1
    
    def get_to_date(self,request,*args):
        obj = Leave_application_db.objects.filter(emp_id_id= str(request.emp_id))
        for i in obj:
            date = (i.to_date)
            d = str(date)
        if d:
            date1 = datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S")
        return date1
    def get_created_date(self,request,*args):
        obj = Leave_application_db.objects.filter(emp_id_id= str(request.emp_id))
        for i in obj:
            date = (i.created_date)
            d = str(date)
        if d:
            date1 = datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S")
        return date1
    class Meta:
        model = Leave_application_db
        fields =['id','emp_id','created_date','leave_type','from_date','to_date','total_leave','leave_application','is_approved']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','full_name','email','profilei_image','phone_number','emergency_no','address']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)