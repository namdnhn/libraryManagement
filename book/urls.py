from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.book_list, name="book_list"),
    path('<int:id>/', views.bookpage, name="detailed_book"),
]