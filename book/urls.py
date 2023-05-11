from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.book_list, name="book_list"),
    path('view/<str:id>/', views.bookpage, name="detailed_book"),
    path('search/', views.search, name='search'),
    path('genre/<str:genre>/', views.view_book_by_genre, name="view_book_by_genre")
]