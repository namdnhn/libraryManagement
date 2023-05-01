from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('add/<int:id>/', views.cart_add, name='cart_add'),
    path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart-detail/',views.cart_detail,name='cart_detail'),
]