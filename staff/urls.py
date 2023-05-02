from django.urls import path
from . import views


app_name = 'staff'
urlpatterns = [
   path('customers', views.customersListView, name="customers_list"),
   path('users/<int:user_id>/', views.user_profile, name='user_profile')
]
