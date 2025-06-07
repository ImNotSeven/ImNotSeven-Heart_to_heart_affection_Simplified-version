from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import pet_list

urlpatterns = [
    #path('', views.index, name='index'),
    path('', pet_list, name='pet_list'),
    path('upload/', views.upload_pet_card, name='upload_pet_card'),
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('apply/<int:pet_id>/',views.pet_apply,name='pet_apply'),
    path('pet_apply/<int:pet_id>/', views.apply_for_pet, name='apply_for_pet'),
    path('my_pets/', views.pet_of_mine,name='pet_of_mine'),
    path('search/', views.pet_search,name='pet_search'),
    path('inform/search/<int:post_id>/', views.pet_search_detail, name="pet_search-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)