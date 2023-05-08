from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, password2=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#custome user
class User(AbstractBaseUser):
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
    inventory_name = models.CharField(max_length=20,blank=True, null=True)
    supplier_name = models.CharField(max_length=20,blank=True, null=True)
    supplier_address =  models.CharField(max_length=20,blank=True, null=True)
    supplier_contact =  models.IntegerField(max_length=10,blank=True, null=True)
    stock_quantity  =  models.CharField(max_length=20,blank=True, null=True)
    costing =   models.CharField(max_length=20,blank=True, null=True)
    is_available  =  models.CharField(max_length=20,default=False)
    def __str__(self):
        return str(self.inventory_name)


class Project_db(models.Model):
    emp = models.ManyToManyField(User)
    project_name =  models.CharField(max_length=200,default=False)
    project_pricing =  models.CharField(max_length=200,default=False)
    inventory =  models.ManyToManyField(Inventory_db, blank=True,null=True ,default=None,related_name='Inventory_db')
    working_status =  models.CharField(max_length=200,default=False)
    project_description  = models.CharField(max_length=200,default=False)
    project_inventory = models.IntegerField(max_length=200,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

class Parts_db(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    part_name = models.CharField(max_length=200,default=False)
    projet_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    working_status =  models.CharField(max_length=200,blank=True,null=True )
    part_description  = models.CharField(max_length=200,default=False)
    total_hours =  models.CharField(max_length=200,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return str(self.id)

class Task_db(models.Model):
   
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    projet_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    parts_id =  models.ForeignKey(Parts_db, on_delete=models.CASCADE)
    parts_quantity = models.IntegerField(max_length=200,default=False)
    opretions = models.CharField(max_length=200,default=False)
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


