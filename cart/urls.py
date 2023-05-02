from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('add/<int:id>/', views.cart_add, name='cart_add'),
    path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart-detail/',views.cart_detail,name='cart_detail'),
    path('transaction-view/',views.view_transaction,name='transaction_view'),
    path('transaction-create/',views.create_transaction,name='transaction_create'),
    path('transaction-list/',views.list_transaction,name='transaction_list'),
]