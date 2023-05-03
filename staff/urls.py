from django.urls import path
from . import views
from home.views import ProfilePage
from book.views import bookpage


app_name = 'staff'
urlpatterns = [
   path('customers', views.customersListView, name="customers_list"),
   path('users/<int:user_id>/', views.user_profile, name='user_profile'),
   path('books/list', views.booksListView, name='books_list'),
   #path('books/add', views.user_profile, name='add_book'),
   path('books/<int:book_id>/', bookpage, name='book_profile'),
   #path('transactions', ProfilePage, name='transactions'),
   path('profile', ProfilePage, name='profile')
]
