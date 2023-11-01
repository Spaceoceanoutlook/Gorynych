from django.urls import path
from .views import index, register, user_login, user_logout

urlpatterns = [
    path('login/', user_login, name='login'),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
]
