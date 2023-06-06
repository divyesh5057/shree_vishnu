from django.urls import path, include
from account.views import *  #UserRegistrationView, UserLoginView, UserLogoutView, ProjectView,PartsView,TaskView,TimesheetView,Get_UserHistory,UserhistoryView,GetAllProject,UpdateProjects,UpdatePartsView,UpdateTaskView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('getallusers/', Getusers.as_view(), name='getallusers'),
    path('updateuser/<int:id>/', UserRegistrationView.as_view(), name='updateuser'),
    path('deleteuser/<int:id>/', UserRegistrationView.as_view(), name='deleteuser'),
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('user-profile/<int:id>', UserProfileAPIView.as_view(), name='user-profile'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('Adminlogin/', AdminLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('project/', ProjectView.as_view(), name='project'),
    path('getallprojects/',GetAllProject.as_view(),name='getallprojects'),
    path('updateprojects/<int:id>/',UpdateProjects.as_view(),name='updateprojects'), 
    path('deleteprojects/<int:id>/',UpdateProjects.as_view(),name='deleteprojects'),

    path('parts/', PartsView.as_view(), name='parts'),
    path('allparts/',Getpart.as_view(),name='allparts'),
    path('updateparts/<int:id>/',UpdatePartsView.as_view(),name='updateparts'),
    path('deleteparts/<int:id>/',UpdatePartsView.as_view(),name='deleteparts'),

    path('task/', TaskView.as_view(), name='task'),
    path('alltasks/',Gettask.as_view(),name='alltasks'),
    path('updatetasks/<int:id>/',UpdateTaskView.as_view(),name='updateparts'),
    path('deletetasks/<int:id>/',UpdateTaskView.as_view(),name='deletetasks'),

    path('inventory/', InventoryView.as_view(), name='InventoryView'),
    path('allinventory/',InventoryView.as_view(),name='alltasks'),
    path('updateinventory/<int:id>/',InventoryView.as_view(),name='updateparts'),
    path('deletetinventory/<int:id>/',InventoryView.as_view(),name='deletetasks'),

    path('transporter/', TransporterView.as_view(), name='transporter'),
    path('alltransporter/',TransporterView.as_view(),name='alltransporter'),
    path('updatetransporter/<int:id>/',TransporterView.as_view(),name='updatetransporter'),
    path('deletetransporter/<int:id>/',TransporterView.as_view(),name='deletetransporter'),

    path('LeaveapplicationView/',LeaveapplicationView.as_view(),name='LeaveapplicationView'),
    path('getallLeaveapplication/',LeaveapplicationView.as_view(),name='getallLeaveapplication'),
    path('Leaveapplicationfilter/',Leaveapplicationfilter.as_view(),name='Leaveapplicationfilter'),
    path('LeaveapplicationViewAdmin/',LeaveapplicationViewAdmin.as_view(),name='LeaveapplicationView'),
    path('LeaveapplicationUpdate/<int:id>/',LeaveapplicationViewAdmin.as_view(),name='LeaveapplicationUpdate'),

    path('timesheet/',TimesheetView.as_view(),name='timesheet'),
    path('get_check_in_check_out/',TimesheetView.as_view(),name='timesheet'),

    path('get_user_history/',Get_UserHistory.as_view()),
    path('get_user_filter/',Get_UserHistory.as_view()),

    path('filterusers/',FilterUsers.as_view(),name='filterusers'),
    path('filterproject/',FilterProject.as_view(),name='filterproject'),
    path('filterpart/',FilterPart.as_view(),name='filterpart'),
    path('filtertask/',FilterTask.as_view(),name='filtertask'),

    path('get_check_in_check_out/',TimesheetView.as_view(),name='GetcheckinAndcheckout'),
    path('ProjectPartView/',UserUpdateApi.as_view(),name='ProjectPartView'),

    path('inventory-pdf/', generate_pdf, name='generate_pdf'),
    path('project-pdf/', project_pdf, name='project_pdf'),
    path('projectdata_pdf/', projectdata_pdf.as_view(), name='projectdata_pdf'),

    path('employee-pdf/', employee_pdf, name='employee_pdf'),
    path('download_pdf/<str:filename>/', download_pdf, name='download_pdf'),
    path('purchase-order-bills/', generate_purchase_order_bills.as_view(), name='purchase_order_bills'),

    path('registers/', UserRegistrationViews.as_view(), name='register'),

    path('projectimgioc/', ProjectImgDocView.as_view(), name='ProjectImgDocView'),
    path('updateprojectimgioc/<int:id>/', ProjectImgDocView.as_view(), name='ProjectImgDocView'),
    path('deleteprojectimgioc/<int:id>/', ProjectImgDocView.as_view(), name='ProjectImgDocView'),

    path('GetAllProjects/', GetAllProjects.as_view(), name='GetAllProjects'),

    path('partimgioc/', PartImgDocView.as_view(), name='partimgioc'),
    path('updatepartimgioc/<int:id>/', ProjectImgDocView.as_view(), name='updatepartimgioc'),
    path('deleteupdatepartimgioc/<int:id>/', ProjectImgDocView.as_view(), name='deleteupdatepartimgioc'),








   


   
]
