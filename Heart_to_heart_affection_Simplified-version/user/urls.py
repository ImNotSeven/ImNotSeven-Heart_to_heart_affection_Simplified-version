from django.urls import path
from . import views
app_name='user'
urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.user_logout, name="logout"),
    path('user_center/', views.user_center, name="user_center"),
    path('user_center/edit_profile/', views.edit_profile, name="edit_profile"),
    path('user_center/change_password/', views.change_password, name="change_password"),
]
