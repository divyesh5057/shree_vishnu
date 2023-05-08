import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import *
from celery import shared_task
from django.http import JsonResponse

@shared_task
def create_random_user_accounts(total):
    print("i am celery task")
    # user = Leave_application_db.objects.get(id=id)
    print("*********",total["emp_id"],total["is_approved"])
    emp_name = total["emp_id"]
    leave_request = total["is_approved"]
    response = {
                "status": "SUCCESS",
                "code": 900,
                "messsage": f" {emp_name} leave request is {leave_request} successfully",
                }
    return response
   