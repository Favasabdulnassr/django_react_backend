from django.urls import path
from .views import RegisterView,RetrieveUpdateDeleteUserView,UserListView,ProfilePictureView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('dataManage/',RetrieveUpdateDeleteUserView.as_view()),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserListView.as_view(), name='user_detail'),
       path('user/profile_picture/', ProfilePictureView.as_view(), name='profile-picture'),


]
