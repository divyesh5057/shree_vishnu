from rest_framework import serializers
from account.models import * #User,Project_db,Parts_db,Task_db,Timesheet_db
from datetime import datetime


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'full_name', 'phone_number', 'emergency_no', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            full_name=validated_data.get('full_name'),
            phone_number=validated_data.get('phone_number'),
            emergency_no=validated_data.get('emergency_no'),
            address=validated_data.get('address'),
        )
        return user

class UserRegistrationSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password','is_admin','role','full_name','phone_number','emergency_no','address']
    #     extra_kwargs = {
    #         'password':{'write_only':True}
    #     }

    # def validate(self, attrs):
    #     password = attrs.get('password')
    #     password2 = attrs.get('password2')

    #     if password != password2:
    #         raise serializers.ValidationError("Password and Confirm Password is not same")
        
    #     return attrs

    # def create(self, validated_data):
    #     print(">>>>>>>>>>>>>>>",validated_data)
    #     return User.objects.create_user(**validated_data)
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            is_admin = validated_data['is_admin'],
            full_name=validated_data.get('full_name'),
            phone_number=validated_data.get('phone_number'),
            emergency_no=validated_data.get('emergency_no'),
            address=validated_data.get('address'),
        )
        return user

class UserGetAll(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['id','username','email','role','full_name','phone_number','emergency_no','address']

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
# class GetproimgdocSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Project_img_doc
#         fields = ['project_doc','project_img']
# class ProjectGetSerializer(serializers.ModelSerializer):
#     inventory = GetInventorySerializer(many=True,read_only=True)    
#     proimg = GetproimgdocSerializer(many=True,read_only=True)    

#     working_status = serializers.SerializerMethodField() 
#     emp = UserlogoutSerializer(many=True,read_only=True) 
#     def get_working_status(self,request,*args):
#         current_user=request
#         user = Project_db.objects.filter(id=str(current_user))
#         for i in user:
#             data = (i.working_status)
#         return data
#     class Meta:
#         model = Project_db
#         fields = ['id','project_name','project_pricing','working_status','project_description','project_inventory','created_at','emp','inventory','proimg']

class Project_img_docSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Project_img_doc
        fields = ['project_doc', 'project_img']

# class ProjectGetSerializer(serializers.ModelSerializer):
#     inventory = GetInventorySerializer(many=True, read_only=True)
#     project_img_doc = Project_img_docSerializer(source='project_img_docs', many=True, read_only=True)
#     emp = UserlogoutSerializer(many=True, read_only=True)
#     working_status = serializers.SerializerMethodField()

#     def get_working_status(self, instance):
#         return instance.working_status

#     class Meta:
#         model = Project_db
#         fields = ['id', 'project_name', 'project_pricing', 'working_status', 'project_description', 'project_inventory', 'created_at', 'emp', 'inventory', 'project_img_doc']

class ProjectGetSerializer(serializers.ModelSerializer):
    inventory = GetInventorySerializer(many=True, read_only=True)
    project_img_doc = Project_img_docSerializer(source='project_img_docs', many=True, read_only=True)
    emp = UserlogoutSerializer(many=True, read_only=True)
    working_status = serializers.SerializerMethodField()

    def get_working_status(self, instance):
        return instance.working_status

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Append lists to emp and inventory fields (as shown in the previous example)
        representation['emp'] = {
            'username': [emp['username'] for emp in representation['emp']]
        }
        representation['inventory'] = {
            'inventory_name': [inv['inventory_name'] for inv in representation['inventory']]
        }
        # Append lists to project_img_doc field
        project_img_doc = representation['project_img_doc']
        updated_project_img_doc = {
            'project_doc': [doc['project_doc'] for doc in project_img_doc],
            'project_img': [doc['project_img'] for doc in project_img_doc]
        }
        representation['project_img_doc'] = [updated_project_img_doc]


        return representation

    class Meta:
        model = Project_db
        fields = ['id', 'project_name', 'project_pricing', 'working_status', 'project_description', 'project_inventory', 'created_at', 'emp', 'inventory', 'project_img_doc']


class ProjectGetSerializerSubadmin(serializers.ModelSerializer):
    inventory = GetInventorySerializer(many=True, read_only=True)
    project_img_doc = Project_img_docSerializer(source='project_img_docs', many=True, read_only=True)
    emp = UserlogoutSerializer(many=True, read_only=True)
    working_status = serializers.SerializerMethodField()

    def get_working_status(self, instance):
        return instance.working_status

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Append lists to emp and inventory fields (as shown in the previous example)
        representation['emp'] = {
            'username': [emp['username'] for emp in representation['emp']]
        }
        representation['inventory'] = {
            'inventory_name': [inv['inventory_name'] for inv in representation['inventory']]
        }
        # Append lists to project_img_doc field
        project_img_doc = representation['project_img_doc']
        updated_project_img_doc = {
            'project_doc': [doc['project_doc'] for doc in project_img_doc],
            'project_img': [doc['project_img'] for doc in project_img_doc]
        }
        representation['project_img_doc'] = [updated_project_img_doc]


        return representation

    class Meta:
        model = Project_db
        fields = ['id', 'project_name', 'working_status', 'project_description', 'project_inventory', 'created_at', 'emp', 'inventory', 'project_img_doc']
# class PartSerializer(serializers.ModelSerializer):
#     projet_id = serializers.SerializerMethodField()
#     emp_id = serializers.SerializerMethodField()

#     def get_projet_id(self,request,*args):
#         id = str(request.projet_id.id)
#         obj = Project_db.objects.get(pk= id)
#         return obj.project_name
    
#     def get_emp_id(self,request,*args):
#         id = str(request.emp_id.id)
#         obj = User.objects.get(pk= id)
#         return obj.username
#     class Meta:
#         model = Parts_db
#         fields = ['id','emp_id','projet_id','part_name','working_status','part_description','total_hours','updated_at']

class PartSerializer(serializers.ModelSerializer):
    # projet_id = serializers.SerializerMethodField()
    # emp_id = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    # updated_at = serializers.SerializerMethodField()

    def get_project_name(self, obj):
        project = obj.projet_id
        return project.project_name if project else None

    def get_username(self, obj):
        employee = obj.emp_id
        return employee.username if employee else None
    
    # def get_updated_at(self,request,*args):
    #     obj = Parts_db.objects.filter(id= str(request.id))
    #     for i in obj:
    #         date = (i.updated_at)
    #         date.date()
    #         d = str(date)
    #     if d:
    #         date1 = datetime.strptime(d[:19], "%Y-%m-%d %H:%M:%S")
        # return date1
    class Meta:
        model = Parts_db
        fields = ['id', 'emp_id', 'projet_id', 'project_name', 'username', 'part_name', 'working_status', 'part_description', 'total_hours', 'updated_at']

class ProjectGetallSerializer(serializers.ModelSerializer):
    emp = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()

    def get_emp(self, obj):
        employees = obj.emp.all()
        return [{'id': employee.id, 'name': employee.username} for employee in employees]

    def get_inventory(self, obj):
        inventories = obj.inventory.all()
        return [{'id': inventory.id, 'name': inventory.inventory_name} for inventory in inventories]

    def get_working_status(self, obj):
        return obj.working_status.capitalize()

    class Meta:
        model = Project_db
        fields = ['id', 'project_name', 'project_pricing', 'working_status', 'project_description', 'project_inventory', 'created_at', 'emp', 'inventory']

class PratsGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parts_db
        fields = '__all__'
class Part_img_docSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Part_img_doc
        fields = ['part_doc', 'part_img']

class PartImgDocSerializer(serializers.ModelSerializer):
    projet_id = serializers.SerializerMethodField()
    emp_id = serializers.SerializerMethodField()
    part_img_doc = Part_img_docSerializer(source='part_img_docs', many=True, read_only=True)


    def get_projet_id(self,request,*args):
        id = str(request.projet_id.id)
        obj = Project_db.objects.get(pk= id)
        return obj.project_name
    
    def get_emp_id(self,request,*args):
        id = str(request.emp_id.id)
        obj = User.objects.get(pk= id)
        return obj.username
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Append lists to emp and inventory fields (as shown in the previous example)
        
        # Append lists to project_img_doc field
        part_img_doc = representation['part_img_doc']
        updated_part_img_doc = {
            'part_doc': [doc['part_doc'] for doc in part_img_doc],
            'part_img': [doc['part_img'] for doc in part_img_doc]
        }
        representation['part_img_doc'] = [updated_part_img_doc]
        return representation

    class Meta:
        model = Parts_db
        fields = ['id','emp_id','projet_id','part_name','working_status','part_description','part_img_doc','total_hours','updated_at']

class TaskaddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task_db
        fields = '__all__'
class TaskSerializer(serializers.ModelSerializer):
    emp_id = serializers.SerializerMethodField()
    projet_id = serializers.SerializerMethodField()
    parts_id = serializers.SerializerMethodField()

    def get_emp_id(self, obj):
        return obj.emp_id.username
    
    def get_projet_id(self, obj):
        return obj.projet_id.project_name
    
    def get_parts_id(self, obj):
        return obj.parts_id.part_name
    class Meta:
        model = Task_db
        fields = ['id','parts_quantity','opretions','part_doc','working_status','is_updated','emp_id','projet_id','parts_id','created_date','updated_date']

class TaskallSerializer(serializers.ModelSerializer):
    emp_id = serializers.SerializerMethodField()
    emp_name = serializers.SerializerMethodField()
    projet_id = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    parts_id = serializers.SerializerMethodField()
    part_name = serializers.SerializerMethodField()

    def get_emp_id(self, obj):
        return obj.emp_id.id

    def get_emp_name(self, obj):
        return obj.emp_id.username

    def get_projet_id(self, obj):
        return obj.projet_id.id

    def get_project_name(self, obj):
        return obj.projet_id.project_name

    def get_parts_id(self, obj):
        return obj.parts_id.id

    def get_part_name(self, obj):
        return obj.parts_id.part_name

    class Meta:
        model = Task_db
        fields = ['id', 'parts_quantity', 'opretions', 'working_status', 'created_date', 'updated_date', 'emp_id', 'emp_name', 'projet_id', 'project_name', 'parts_id', 'part_name']

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
        return data
    
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
        fields = ['id','project_name']

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
    # from_date = serializers.SerializerMethodField()
    # to_date = serializers.SerializerMethodField()
    # created_date = serializers.SerializerMethodField()
    def get_emp_id(self,request,*args):
        obj = User.objects.get(pk= str(request.emp_id))
        return obj.username
    class Meta:
        model = Leave_application_db
        fields =['id','emp_id','created_date','leave_type','from_date','to_date','total_leave','leave_application','is_approved']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','full_name','email','profilei_image','phone_number','emergency_no','address']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserUpdate_dbSerializer(serializers.ModelSerializer):
    emp_id = serializers.SerializerMethodField()
    emp_name = serializers.SerializerMethodField()
    projet_id = serializers.SerializerMethodField()
    projet_name = serializers.SerializerMethodField()
    part_id = serializers.SerializerMethodField()
    part_name = serializers.SerializerMethodField()
    task_id = serializers.SerializerMethodField()
    task_name = serializers.SerializerMethodField()

    def get_emp_id(self, obj):
        return obj.emp_id.id

    def get_emp_name(self, obj):
        return obj.emp_id.username

    def get_projet_id(self, obj):
        return obj.projet_name.id

    def get_projet_name(self, obj):
        return obj.projet_name.project_name

    def get_part_id(self, obj):
        return obj.part_name.id

    def get_part_name(self, obj):
        return obj.part_name.part_name

    def get_task_id(self, obj):
        return obj.task_name.id

    def get_task_name(self, obj):
        return obj.task_name.opretions

    class Meta:
        model = UserUpdate_db
        fields = [
            'id',
            'emp_id',
            'emp_name',
            'projet_id',
            'projet_name',
            'part_id',
            'part_name',
            'task_id',
            'task_name',
            'part_description',
            'working_status',
            'total_hours'
        ]



class ProjectimgdocSendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project_img_doc
        fields = '__all__'

class PartimgdocSendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part_img_doc
        fields = '__all__'