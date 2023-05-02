from django.urls import path
from . import views

app_name = 'staff'
urlpatterns = [
   path('staffs', views.staffsListView, name="staffs_list"),
   path('users/<int:user_id>/', views.user_profile, name='user_profile')
]
