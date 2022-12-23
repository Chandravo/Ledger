from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('create_room/',views.create_room,name='create_room'),
    path('join_room/',views.join_room,name='join_room'),

]