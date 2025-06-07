from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.blog_page, name='blog_page'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # 显示具体文章和评论
    path('like/<int:pk>/', views.like_post, name='like_post'),  # 点赞功能
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
