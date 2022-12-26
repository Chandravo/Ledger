from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('create_room/',views.create_room,name='create_room'),
    path('join_room/',views.join_room,name='join_room'),
    path('room/<str:room_key>/',views.room,name='room'),
    path('room/<str:room_key>/delete/',views.delete_room,name='delete_room'),
    path('room/<str:room_key>/create_money_request',views.create_money_request,name='create_money_request'),
    path('room/<str:room_key>/accepted_money_requests',views.accepted_money_requests,name='accepted_money_requests'),
    path('delete_money_request/',views.delete_money_request,name='delete_money_request'),
    path('accept_money_request/',views.accept_money_request,name='accept_money_request'),
    
]