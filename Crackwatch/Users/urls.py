from django.urls import path, include
from . import views

app_name = "Users"

urlpatterns = [
    path('<slug:user>/', views.UsersView, name="UsersHome"),
    path('ranks/<slug:user>', views.AllRanksView, name="UsersRanks"),
]
