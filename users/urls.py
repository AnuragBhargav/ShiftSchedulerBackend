from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserListCreateAPIView,UserDetailAPIView

app_name = 'users'

urlpatterns = [
    path('users/', UserRegistrationAPIView.as_view(), name="list"),
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
    path('users/add_info/', UserListCreateAPIView.as_view(), name="add_user_info"),
    path('users/user_info/', UserDetailAPIView.as_view(), name="user_info"),
]
