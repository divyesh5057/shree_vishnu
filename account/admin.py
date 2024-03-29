from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

from .models import *

class UserModelAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('id', 'username','email', 'is_admin', 'is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(Inventory_db)
admin.site.register(Project_db)
admin.site.register(Parts_db)
admin.site.register(Task_db)
admin.site.register(Timesheet_db)
admin.site.register(Transporter_db)
