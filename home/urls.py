from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
   path('', views.index, name='home'),
   path('login', views.LoginPage, name='login'),
   path('signup', views.SignupPage, name='signup'),
   path('logout', views.LogoutPage, name='logout'),
   path('home/profile', views.ProfilePage)
]
