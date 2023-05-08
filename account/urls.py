from django.urls import path, include
from account.views import * #UserRegistrationView, UserLoginView, UserLogoutView, ProjectView,PartsView,TaskView,TimesheetView,Get_UserHistory,UserhistoryView,GetAllProject,UpdateProjects,UpdatePartsView,UpdateTaskView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('getallusers/', UserRegistrationView.as_view(), name='getallusers'),
    path('updateuser/<int:id>/', UserRegistrationView.as_view(), name='updateuser'),
    path('deleteuser/<int:id>/', UserRegistrationView.as_view(), name='deleteuser'),
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('project/', ProjectView.as_view(), name='project'),
    path('getallprojects/',Getproject.as_view(),name='getallprojects'),
    path('updateprojects/<int:id>/',UpdateProjects.as_view(),name='updateprojects'), 
    path('deleteprojects/<int:id>/',UpdateProjects.as_view(),name='deleteprojects'),

    path('parts/', PartsView.as_view(), name='parts'),
    path('allparts/',PartsView.as_view(),name='allparts'),
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

    path('GetcheckinAndcheckout/',GetcheckinAndcheckout.as_view(),name='GetcheckinAndcheckout'),
    path('ProjectPartView/',UserUpdateApi.as_view(),name='ProjectPartView')




   


   
]
