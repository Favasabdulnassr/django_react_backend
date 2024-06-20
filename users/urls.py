from django.urls import path
from .views import RegisterView,RetrieveUpdateDeleteUserView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('dataManage/',RetrieveUpdateDeleteUserView.as_view())
]
