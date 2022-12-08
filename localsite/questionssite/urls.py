from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', TableListTest.as_view(), name="home"),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('result/<int:pk>', ResultTest.as_view(), name="result"),
    path('pass/<int:pk1>/', DetailsTest.as_view(), name="pass"),
    path('pass/<int:pk1>/<int:pk2>', DetailsTest.as_view(), name="pass"),
    ]