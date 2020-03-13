from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserListCreateAPIView,UserDetailAPIView , ShiftScheduleListCreateAPIView,shift_schedule_view,user_info_with_shifts, shifts_info_user,user_shift,users_project_shift

app_name = 'users'

urlpatterns = [
    path('users/', UserRegistrationAPIView.as_view(), name="list"),
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
    path('users/user_info/', UserListCreateAPIView.as_view(), name="user_info"),
    path('users/shifts/', ShiftScheduleListCreateAPIView.as_view(), name="user_shift_info"),
    path('users/user_shift_info/',shift_schedule_view , name="add_user_info"),
    path('users/user_info_shift_info/', user_info_with_shifts, name="add_user_info"),
    path('users/shift_details/<project_id>/<dd>/<mm>/<yyyy>', shifts_info_user, name="shifts_info_user"),
    path('users/<user_id>/<dd>/<mm>/<yyyy>', user_shift, name="user_shift"),
    path('users/<project_id>/<shift_name>/<dd>/<mm>/<yyyy>', users_project_shift, name="users_project_shift"),
    # path('users/user_info_edit/', UserDetailAPIView.as_view(), name="user_info"),
]
