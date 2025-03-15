from django.conf.urls.static import static
from django.urls import path
from shop import views as shop_views
from cart import views as cart_views
from django.conf import settings



app_name="shop"

urlpatterns = [
    path('', shop_views.shop, name="shop"),
    #path('home/', shop_views.shop, name="shop"),
    path('<int:每个类别_id>/', shop_views.category, name="category"),
    path('<int:每个类别_id>/<int:每件商品_id>/', shop_views.detail, name="detail"),
    path('shop/search/<int:post_id>/', shop_views.search_detail, name="search-detail"),
    path('cart/add_cart/<int:商品_id>/',cart_views.add_cart, name="add_cart"),
    path('cart/show_cart/',cart_views.show_cart, name="show_cart"),
    path('cart/remove_cart/',cart_views.remove_cart, name="remove_cart"),
    path('cart/order/',cart_views.order, name="order"),
    path('cart/submit_order/',cart_views.submit_order, name="submit_order"),
    path('cart/success/',cart_views.success, name="success"),
    path('shop/search/', shop_views.search, name='search')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
