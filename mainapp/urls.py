# mainapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Generic product list view by category
    path('products/<str:category>/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # for later

    path('cart/', views.cart_view, name='cart'),
    
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),


    path('checkout/', views.checkout_page, name='checkout'),

]
