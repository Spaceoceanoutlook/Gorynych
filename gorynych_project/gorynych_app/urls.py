from django.urls import path
from .views import index, register, user_login, user_logout, get_record_html, statistics

urlpatterns = [
    path('login/', user_login, name='login'),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('game_detail/<str:user>/', get_record_html, name='get_record_html'),
    path('statistics/<str:user>/', statistics, name='statistics'),
]
