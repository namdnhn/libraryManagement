from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.book_list, name="book_list"),
    path('<str:id>/', views.bookpage, name="detailed_book"),
    path('search/', views.search, name='search'),
]