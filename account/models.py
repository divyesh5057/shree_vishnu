from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role=None, **extra_fields):
        # Create and save a regular User
        if not username:
            raise ValueError("The Username field must be set")
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # Create and save a superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


#custome user
class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Subadmin', 'Subadmin'),
        ('Employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default="Employee")
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(unique=True, max_length=200)
    full_name = models.CharField(max_length=60,null=True,blank=True)
    profilei_image = models.ImageField(upload_to='profileimages/', blank=True, null=True)
    phone_number= models.CharField(max_length=10,null=True,blank=True)
    emergency_no = models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=60,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

class Inventory_db(models.Model):
    inventory_name = models.CharField(max_length=100,blank=False, null=False,default=False)
    stock_quantity  =  models.CharField(max_length=100,blank=False, null=False,default=False)
    costing =   models.CharField(max_length=100,blank=False, null=False,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.inventory_name)
    
class Supplier_db(models.Model):
    supplier_name = models.CharField(max_length=255)
    supplier_email = models.EmailField(unique=True)
    supplier_phone_number = models.CharField(max_length=20)
    supplier_address = models.TextField()
    supplier_description = models.TextField(default='')

    def __str__(self):
        return self.supplier_name

class Customer_db(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100, default='')
    address = models.TextField()
    customer_description = models.TextField(default='')
    
    def __str__(self):
        return self.name

class Project_db(models.Model):
    emp = models.ManyToManyField(User, blank=True,null=True ,default=None)
    customer_id = models.ForeignKey(Customer_db, on_delete=models.CASCADE,blank=True,null=True,related_name='Project_db')
    project_name =  models.CharField(max_length=200,default=False)
    project_pricing =  models.CharField(max_length=200,default=False)
    working_status =  models.CharField(max_length=200,default=False)
    project_description  = models.TextField(default=False)
    project_doc = models.FileField(upload_to='project_doc/', blank=True, null=True)
    estimation_time = models.DateTimeField(blank=True, null=True)
    secondary_inventory =  models.ManyToManyField(Inventory_db, blank=True,null=True ,default=None,related_name='Inventory_db')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

class secondary_inventory_stock(models.Model):
    project_id = models.ForeignKey(Project_db, on_delete=models.CASCADE,blank=True,null=True,related_name='secondary_inventory_stock')
    secondary_inventory =  models.ForeignKey(Inventory_db, on_delete=models.CASCADE,blank=True,null=True,related_name='secondary_inventory')
    stock_quantity  =  models.CharField(max_length=100,blank=False, null=False,default=False)

class primary_inventory(models.Model):
    project_id = models.ForeignKey(Project_db, on_delete=models.CASCADE,blank=True,null=True,related_name='Project_db')
    supplier_id = models.ManyToManyField(Supplier_db, blank=True,null=True ,default=None)
    name = models.CharField(max_length=100,blank=False, null=False)


class Parts_db(models.Model):
    emp_id = models.ManyToManyField(User, blank=True,null=True ,default=None)
    part_name = models.CharField(max_length=200,default=False)
    project_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    working_status =  models.CharField(max_length=200,blank=True,null=True )
    part_description  = models.TextField(default=False)
    total_hours =  models.CharField(max_length=200,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    part_doc = models.FileField(upload_to='part_doc/', blank=True, null=True)
    def __str__(self):
        return str(self.id)
    
class Task_db(models.Model):
    Status_choices = (
                    ('High', 'High'),
                        ('Medium', 'Hedium'),
                        ('Low', 'Low'),
                        )
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True, related_name='tasks')
    project_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    parts_id =  models.ForeignKey(Parts_db, on_delete=models.CASCADE)
    opretions = models.CharField(max_length=200,default=False)
    working_status =  models.CharField(max_length=200,default=False)
    total_hours = models.IntegerField(default=0)
    is_poverty = models.CharField(max_length = 20,choices=Status_choices,default='Medium')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_role  =  models.BooleanField(max_length=200,default=True)
    is_task  =  models.BooleanField(max_length=200,default=False)
    def __str__(self):
        return str(self.id)
 
class UserUpdate_db(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    project_name = models.ForeignKey(Project_db, on_delete=models.CASCADE,blank=True, null=True)
    part_name = models.ForeignKey(Parts_db, on_delete=models.CASCADE,blank=True, null=True)
    task_name = models.ForeignKey(Task_db,on_delete=models.CASCADE,blank=True, null=True)
    working_status =  models.CharField(max_length=200,blank=True,null=True )
    part_description  = models.CharField(max_length=200,default=False)
    task_img = models.ImageField(upload_to='taskimages/', blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    total_hours =  models.CharField(max_length=200,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
        
    def save(self, *args, **kwargs):
        # Custom save logic
        super().save(*args, **kwargs)  # Call the parent save method

class Transporter_db(models.Model):
    name = models.CharField(max_length=20,blank=True, null=True)
    contact_number = models.CharField(max_length=20,blank=True, null=True)
    vehicle_type = models.CharField(max_length=20,blank=True, null=True)


