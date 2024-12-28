from django.urls import path
from . import views

urlpatterns = [
    path('get_users', views.getUsers),
    path('register', views.registerUser),
    path('get_user/<str:pk>', views.getUser),
    path('update_user/<str:pk>', views.updateUser),
    path('delete_user/<str:pk>', views.deleteUser)
]


