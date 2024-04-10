
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path('',views.home,name="home"),
    path('rooms/<str:pk>/',views.rooms,name="rooms"),
    path('create-room/',views.CreateRoom,name="create-room"),
    path('update-room/<str:pk>/',views.UpdateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.DeleteRoom,name="delete-room"),
    path('delete-message/<str:pk>/',views.DeleteMessage,name="delete-message"),
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutuser,name="logout"),
    path('register/',views.registerpage,name="register"),
    path('user-profile/<str:pk>',views.userprofile,name="user-profile"),
]
