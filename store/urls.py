from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
   path('staffs', views.staffsListView, name="staffs_list"),
   path('staff_register', views.staffRegister, name="staff_register"),
   path('staffs/<int:user_id>/', views.staff_profile, name='staff_profile')
]
