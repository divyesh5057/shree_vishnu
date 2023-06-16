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
    class Meta:
        model = User
        fields = ['username', 'email', 'password','is_admin','role','full_name','phone_number','emergency_no','address']
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

class Project_GetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project_db
        fields = ['id', 'project_name', 'working_status', 'project_description', 'project_doc']

class Part_list_Serializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()

    def get_project_name(self, obj):
        project = obj.project_id
        return project.project_name if project else None

    class Meta:
        model = Parts_db
        fields = ['id', 'project_id', 'project_name','part_name', 'working_status', 'part_description','part_doc']

class PartSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    def get_project_name(self, obj):
        project = obj.project_id
        return project.project_name if project else None

    def get_username(self, obj):
        employee = obj.emp_id
        return employee.username if employee else None
    class Meta:
        model = Parts_db
        fields = ['id', 'emp_id', 'project_id', 'project_name', 'username', 'part_name', 'working_status', 'part_description', 'total_hours', 'updated_at']


class PratsGetSerializer(serializers.ModelSerializer):
    emp_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    part_doc = serializers.FileField(required=False)
    class Meta:
        model = Parts_db
        fields = '__all__'

class PartImgDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parts_db
        fields = ['id','emp_id','project_id','part_name','working_status','part_description','part_doc','total_hours','updated_at']

class TaskaddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task_db
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    emp_id = serializers.SerializerMethodField()
    # project_id = serializers.SerializerMethodField()
    # parts_id = serializers.SerializerMethodField()

    def get_emp_id(self, obj):
        if obj.emp_id:
            return obj.emp_id.username
        return None
    
    # def get_project_id(self, obj):
    #     return obj.project_id.project_name
    
    # def get_parts_id(self, obj):
    #     return obj.parts_id.part_name
    class Meta:
        model = Task_db
        fields = ['id','opretions','working_status','is_role','emp_id','project_id','parts_id','total_hours','created_date','is_poverty','is_task','updated_date']

class TaskallSerializer(serializers.ModelSerializer):
    emp_id = serializers.SerializerMethodField()
    emp_name = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    parts_id = serializers.SerializerMethodField()
    part_name = serializers.SerializerMethodField()

    def get_emp_id(self, obj):
        if hasattr(obj, 'emp_id') and obj.emp_id:
            return obj.emp_id.id
        return None
    def get_emp_name(self, obj):
        if obj.emp_id:
            return obj.emp_id.username
        return None
    def get_project_id(self, obj):
        return obj.project_id.id
    def get_project_name(self, obj):
        return obj.project_id.project_name
    def get_parts_id(self, obj):
        return obj.parts_id.id
    def get_part_name(self, obj):
        return obj.parts_id.part_name

    class Meta:
        model = Task_db
        fields = ['id','opretions', 'working_status', 'created_date', 'updated_date', 'emp_id', 'emp_name', 'project_id', 'project_name', 'parts_id', 'part_name','is_poverty']

class TaskGetSerializer(serializers.ModelSerializer):
    working_status = serializers.SerializerMethodField() 
    project_id = serializers.SerializerMethodField() 
    parts_id = serializers.SerializerMethodField() 


    def get_working_status(self,request,*args):
        current_user=request
        user = Task_db.objects.filter(id=str(current_user))
        for i in user:
            data = (i.working_status)
        return data
    
    def get_project_id(self,request,*args):
        current_user=request
        user = Task_db.objects.filter(id=str(current_user))
        
        for i in user:
            data = (i.project_id)
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
        fields = ['id','emp_id','parts_quantity','opretions','working_status','created_date','is_poverty','updated_date','project_id','parts_id','is_updated']


class InventoryAllSerializer(serializers.ModelSerializer):

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
    # project_id = serializers.SerializerMethodField()

    class Meta:
        model = Parts_db
        fields = ['id','project_id','part_name','working_status','part_description','updated_at']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','full_name','email','profilei_image','phone_number','emergency_no','address']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserUpdate_dbSerializer(serializers.ModelSerializer):
    emp_id = serializers.SerializerMethodField()
    emp_name = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    part_id = serializers.SerializerMethodField()
    part_name = serializers.SerializerMethodField()
    task_id = serializers.SerializerMethodField()
    task_name = serializers.SerializerMethodField()

    def get_emp_id(self, obj):
        return obj.emp_id.id

    def get_emp_name(self, obj):
        return obj.emp_id.username

    def get_project_id(self, obj):
        return obj.project_name.id

    def get_project_name(self, obj):
        return obj.project_name.project_name

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
            'project_id',
            'project_name',
            'part_id',
            'part_name',
            'task_id',
            'task_name',
            'part_description',
            'working_status',
            'total_hours'
        ]



class PrimaryInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = primary_inventory
        fields = ['name']

class ProjectDBSerializer(serializers.ModelSerializer):
    emp = serializers.SerializerMethodField()
    secondary_inventory = serializers.SerializerMethodField()
    primary_inventory = PrimaryInventorySerializer(source='Project_db',many=True, read_only=True)

    def get_emp(self, obj):
        employees = obj.emp.all()
        return [{'id': employee.id, 'name': employee.username} for employee in employees]

    def get_secondary_inventory(self, obj):
        inventories = obj.secondary_inventory.all()
        return [{'id': inventory.id, 'name': inventory.inventory_name} for inventory in inventories]

    class Meta:
        model = Project_db
        fields = ['id','customer_id','project_name','project_pricing','working_status','project_description','project_doc','estimation_time','secondary_inventory','emp','primary_inventory']

class Projects(serializers.ModelSerializer):
    class Meta:
        model = Project_db
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory_db
        fields = ['id','inventory_name', 'stock_quantity', 'costing']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier_db
        fields = ['supplier_name']

class SecondaryInventoryStockSerializer(serializers.ModelSerializer):
    # secondary_inventory = InventorySerializer()
    class Meta:
        model = secondary_inventory_stock
        fields = ['secondary_inventory', 'stock_quantity']

class PrimaryInventorySerializer(serializers.ModelSerializer):
    supplier_id = SupplierSerializer(many=True)
    class Meta:
        model = primary_inventory
        fields = ['name', 'supplier_id']
        
class ProjectsDBAdminSerializer(serializers.ModelSerializer):
    emp = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(read_only=True)
    primary_inventory = serializers.SerializerMethodField()
    secondary_inventory = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()

    def get_primary_inventory(self, obj):
        inventories = primary_inventory.objects.filter(project_id=obj.id)
        serialized_inventories = []
        for inventory in inventories:
            suppliers = inventory.supplier_id.values_list('id', flat=True)
            serialized_inventory = {
                'supplier': list(suppliers),
                'inventoryName': inventory.name
            }
            serialized_inventories.append(serialized_inventory)
        return serialized_inventories

    def get_secondary_inventory(self, obj):
        stocks = secondary_inventory_stock.objects.filter(project_id=obj.id)
        inventory_ids = stocks.values_list('secondary_inventory', flat=True)
        return list(inventory_ids)

    def get_stock(self, obj):
        stocks = secondary_inventory_stock.objects.filter(project_id=obj.id)
        serialized_stocks = []
        for stock in stocks:
            serialized_stock = {
                'inventory_id': stock.secondary_inventory.id,
                'stock_quantity': stock.stock_quantity
            }
            serialized_stocks.append(serialized_stock)
        return serialized_stocks

    class Meta:
        model = Project_db
        fields = ['id','emp', 'customer_id', 'project_name', 'project_pricing', 'working_status',
                  'project_description','project_doc', 'estimation_time', 'primary_inventory',
                  'secondary_inventory', 'stock']


class ProjectsDBSubAdminSerializer(serializers.ModelSerializer):
    emp = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(read_only=True)
    primary_inventory = serializers.SerializerMethodField()
    secondary_inventory = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()

    def get_primary_inventory(self, obj):
        inventories = primary_inventory.objects.filter(project_id=obj.id)
        serialized_inventories = []
        for inventory in inventories:
            suppliers = inventory.supplier_id.values_list('id', flat=True)
            serialized_inventory = {
                'supplier': list(suppliers),
                'inventoryName': inventory.name
            }
            serialized_inventories.append(serialized_inventory)
        return serialized_inventories

    def get_secondary_inventory(self, obj):
        stocks = secondary_inventory_stock.objects.filter(project_id=obj.id)
        inventory_ids = stocks.values_list('secondary_inventory', flat=True)
        return list(inventory_ids)

    def get_stock(self, obj):
        stocks = secondary_inventory_stock.objects.filter(project_id=obj.id)
        serialized_stocks = []
        for stock in stocks:
            serialized_stock = {
                'inventory_id': stock.secondary_inventory.id,
                'stock_quantity': stock.stock_quantity
            }
            serialized_stocks.append(serialized_stock)
        return serialized_stocks

    class Meta:
        model = Project_db
        fields = ['id','emp', 'customer_id', 'project_name','working_status',
                  'project_description', 'project_doc','estimation_time', 'primary_inventory',
                  'secondary_inventory', 'stock']



#-----------------------------------------Tejas work ---------------------------------

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_db
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier_db
        fields = '__all__'