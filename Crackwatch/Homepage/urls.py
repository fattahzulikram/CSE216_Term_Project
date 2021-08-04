from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomepageView, name="index"),
    path('login/', views.LoginView, name="Login"),
    path('signup/', views.RegisterView, name="Register"),
]
