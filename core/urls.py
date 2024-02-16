from django.urls import path
from .views import HomeView,  checkout, CakeView, add_to_cart, ShopView, remove_from_cart, OrderSummary, remove_single_item_from_cart


urlpatterns = [
    path('',HomeView.as_view(), name='index'),
    path('shop', ShopView.as_view(), name='shop'),
    path('cart', OrderSummary.as_view(), name='cart'),
    path('checkout', checkout, name='checkout'),
    path('cake/<slug>', CakeView.as_view(), name='cake'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
]