from django.urls import path
from . import views
from home.views import ProfilePage


app_name = 'staff'
urlpatterns = [
   path('customers', views.customersListView, name="customers_list"),
   path('users/<int:user_id>/', views.user_profile, name='user_profile'),
   path('profile', ProfilePage, name='profile')
]
