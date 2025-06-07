from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home_page'),
    path('home/', views.home, name='home_page'),
    # path('gradio/', views.my_view, name='gradio'),
    path('index/', views.index, name='index'),
    path('clear-images/', views.clear_images_on_exit, name='clear_images_on_exit'),
]
