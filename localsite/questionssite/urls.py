from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', TableListTest.as_view(), name="home"),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('pass/<int:pk>', DetailsTest.as_view(), name="pass"),
    ]