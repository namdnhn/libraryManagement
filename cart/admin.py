from django.contrib import admin
from .models import Transaction, TransactionItem, Cart, CartItem

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
