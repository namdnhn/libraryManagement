from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('add/<str:id>/', views.cart_add, name='cart_add'),
    path('item_clear/<str:id>/', views.item_clear, name='item_clear'),
    path('cart-detail/',views.cart_detail,name='cart_detail'),
]