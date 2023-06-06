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
    inventory_name = models.CharField(max_length=100,blank=False, null=False,default="svdt")
    supplier_name = models.CharField(max_length=100,blank=False, null=False,default="svdt")
    supplier_address =  models.CharField(max_length=100,blank=False, null=False,default="svdt")
    supplier_contact = models.CharField(max_length=100,null=False,blank=False,default="svdt")
    stock_quantity  =  models.CharField(max_length=100,blank=False, null=False,default="svdt")
    costing =   models.CharField(max_length=100,blank=False, null=False,default="svdt")
    is_available  =  models.CharField(max_length=100,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.inventory_name)


class Project_db(models.Model):
    emp = models.ManyToManyField(User, blank=True,null=True ,default=None)
    project_name =  models.CharField(max_length=200,default=False)
    project_pricing =  models.CharField(max_length=200,default=False)
    inventory =  models.ManyToManyField(Inventory_db, blank=True,null=True ,default=None,related_name='Inventory_db')
    working_status =  models.CharField(max_length=200,default=False)
    project_description  = models.CharField(max_length=200,default=False)
    project_inventory = models.IntegerField(max_length=200,default=False)
    estimation_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

class Project_img_doc(models.Model):
    project_id =  models.ForeignKey(Project_db, on_delete=models.CASCADE,blank=True,null=True,related_name='project_img_docs')
    project_doc = models.FileField(upload_to='project_doc/', blank=True, null=True)
    project_img = models.ImageField(upload_to='project_img/', blank=True, null=True)
    def __str__(self):
        return str(self.project_doc)

class Parts_db(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    part_name = models.CharField(max_length=200,default=False)
    projet_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    working_status =  models.CharField(max_length=200,blank=True,null=True )
    part_description  = models.CharField(max_length=200,default=False)
    total_hours =  models.CharField(max_length=200,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
    
class Part_img_doc(models.Model):
    part_id =  models.ForeignKey(Parts_db, on_delete=models.CASCADE,blank=True, null=True,related_name='part_img_docs')
    part_doc = models.FileField(upload_to='part_doc/', blank=True, null=True)
    part_img = models.ImageField(upload_to='part_img/', blank=True, null=True)

class Task_db(models.Model):
   
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    projet_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    parts_id =  models.ForeignKey(Parts_db, on_delete=models.CASCADE)
    parts_quantity = models.IntegerField(max_length=200,default=False)
    opretions = models.CharField(max_length=200,default=False)
    part_doc = models.FileField(upload_to='part_dox/', blank=True, null=True)
    working_status =  models.CharField(max_length=200,default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_updated  =  models.BooleanField(max_length=200,default=False)
    def __str__(self):
        return str(self.id)
 
class Timesheet_db(models.Model):
    # id = models.IntegerField(primary_key = True)
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    projet_id = models.ManyToManyField(Project_db, blank=True,null=True, default=None,related_name='project_id')
    parts_id =  models.ManyToManyField(Parts_db, blank=True,null=True ,default=None,related_name='parts_db')
    task_id =  models.ManyToManyField(Task_db, blank=True,null=True, default=None,related_name='task_db')
    hours_for_the_day =  models.CharField(max_length=200,default=False)
    check_in =models.BooleanField(default=False)
    check_in_time = models.DateTimeField(blank=True, null=True)
    check_out = models.BooleanField(default=False)
    check_out_time = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return str(self.id)
    

Status_choices = (
   ('Approved', 'Approved'),
     ('Rejected', 'Rejected'),
    ('Pending', 'Pending'),)

class Leave_application_db(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)
    leave_type = models.CharField(max_length=200,blank=True, null=True)
    total_leave = models.CharField(max_length=200,blank=True,null=True)
    leave_application =  models.TextField(max_length=200,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.CharField(max_length = 20,choices=Status_choices,default='Pending')


class UserUpdate_db(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    projet_name = models.ForeignKey(Project_db, on_delete=models.CASCADE,blank=True, null=True)
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


