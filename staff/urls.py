from django.urls import path
from . import views
from home.views import ProfilePage


app_name = 'staff'
urlpatterns = [
   path('customers', views.customersListView, name="customers_list"),
   path('users/<int:user_id>/', views.user_profile, name='user_profile'),
   path('books/list', views.booksListView, name='books_list'),
   path('books/add', views.addBookView, name='add_book'),
   path('books/<str:id>/', views.editBookProfile, name='book_profile'),
   path('transactions/<int:id>/', views.transactionProfile, name='transaction_profile'),
   path('handover', views.handOverTransactionView, name='book_handover'),
   path('return', views.returnBooksView, name='book_return'),
   path('profile', ProfilePage, name='profile')
]
