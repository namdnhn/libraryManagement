from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
   path('add-comment/<str:book_id>/', views.add_comment, name='add_comment'),
   path('add-rating/<str:book_id>/', views.add_rating, name="add_rating"),
   path('edit-rating/<str:book_id>/', views.edit_rating, name="edit_rating"),
]