from django.urls import path, include
from account.views import *  #UserRegistrationView, UserLoginView, UserLogoutView, ProjectView,PartsView,TaskView,TimesheetView,Get_UserHistory,UserhistoryView,GetAllProject,UpdateProjects,UpdatePartsView,UpdateTaskView

urlpatterns = [
# -----------------------User Registration --------------------------------------------
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('getallusers/', Getusers.as_view(), name='getallusers'),
    path('getall_users/', Get_users.as_view(), name='getall_users'),
    path('updateuser/<int:id>/', UserRegistrationView.as_view(), name='updateuser'),
    path('deleteuser/<int:id>/', UserRegistrationView.as_view(), name='deleteuser'),
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('user-profile/<int:id>', UserProfileAPIView.as_view(), name='user-profile'),
# ----------------------User login ------------------------------------------------------
    path('login/', UserLoginView.as_view(), name='login'),
# ----------------------User Admin ------------------------------------------------------
    path('Adminlogin/', AdminLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
# ~~~~~~~~~~~~~~~~~~~~~~~~~Project Model Api~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    path('project-db/', ProjectDBView.as_view(), name='project-db'),
    path('projectall-db/', ProjectAllDBView.as_view(), name='project-db'),
    path('project-db/<int:pk>/', ProjectDBView.as_view(), name='project-db'),
    path('primary-inventory/', PrimaryInventoryView.as_view(), name='primary-inventory'),
    path('project-user/',ProjectUsers.as_view(),name='project-user'),
# ~~~~~~~~~~~~~~~~~~~~~~~~~Part Model Api~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    path('parts/', PartsView.as_view(), name='parts'),
    path('allparts/',Getpart.as_view(),name='allparts'),
    path('all_parts/',Get_part.as_view(),name='all_parts'),
    path('updateparts/<int:id>/',UpdatePartsView.as_view(),name='updateparts'),
    path('deleteparts/<int:id>/',UpdatePartsView.as_view(),name='deleteparts'),
    path('project_parts/<int:id>/', PartslistView.as_view(), name='parts-list'), #tejas
# ~~~~~~~~~~~~~~~~~~~~~~~~~Task Model Api~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    path('task/', TaskView.as_view(), name='task'),
    path('alltasks/',Gettask.as_view(),name='alltasks'),
    path('all_tasks/',Get_task.as_view(),name='all_tasks'), #without pagination
    path('updatetasks/<int:id>/',UpdateTaskView.as_view(),name='updateparts'),
    path('deletetasks/<int:id>/',UpdateTaskView.as_view(),name='deletetasks'),
    path('parts_tasklist/<int:id>/', Parts_TaskListView.as_view(), name='partstasklist'),
# ~~~~~~~~~~~~~~~~~~~~~~~~~Task Model Api~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    path('taskuser/', TaskViewUser.as_view(), name='task'),
    path('updatetasksuser/<int:id>/',TaskViewUser.as_view(),name='updateparts'),
    path('deletetasksuser/<int:id>/',TaskViewUser.as_view(),name='deletetasks'),
# ~~~~~~~~~~~~~~~~~~~~~~~~~InventoryView Model Api~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    path('inventory/', InventoryView.as_view(), name='InventoryView'),
    path('allinventory/',InventoryView.as_view(),name='alltasks'),
    path('updateinventory/<int:id>/',InventoryView.as_view(),name='updateparts'),
    path('deletetinventory/<int:id>/',InventoryView.as_view(),name='deletetasks'),
# ~~~~~~~~~~~~~~~~~~~~~~~~~transporter Model Api~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    path('transporter/', TransporterView.as_view(), name='transporter'),
    path('alltransporter/',TransporterView.as_view(),name='alltransporter'),
    path('updatetransporter/<int:id>/',TransporterView.as_view(),name='updatetransporter'),
    path('deletetransporter/<int:id>/',TransporterView.as_view(),name='deletetransporter'),
# ~~~~~~~~~~~~~~~~~~~~~~~~~Filter  Api~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    path('filterusers/',FilterUsers.as_view(),name='filterusers'),
    path('filterproject/',FilterProject.as_view(),name='filterproject'),
    path('filterpart/',FilterPart.as_view(),name='filterpart'),
    path('filtertask/',FilterTask.as_view(),name='filtertask'),
# ----------------------------------------------------------------------------------
    # path('ProjectPartView/',UserUpdateApi.as_view(),name='ProjectPartView'),
# ----------------------------------customers model api -------------------
    path('customers/', Customer.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', Customer.as_view(), name='customer-retrieve-update-destroy'),
# ----------------------------------supplier model api -------------------
    path('supplier/', Supplier.as_view(), name='supplier-list-create'),
    path('supplier/<int:pk>/', Supplier.as_view(), name='supplier-retrieve-update-destroy'),
# ----------------------------------Cout model api -------------------
    path('counts/', TotalCountAPIView.as_view(), name='total_counts'),
# ----------------------------------Project_view model api -------------------
    path('Project_view/', Project_view.as_view(), name='Project_view'),
# -----------------------------pdf for report-------------------------------------------
    path('download_pdf/<str:filename>/', download_pdf, name='download_pdf'),
    path('projectdata_pdf/', projectdata_pdf.as_view(), name='projectdata_pdf'),






   


   
]
