from django.urls import path, include
from . import views

app_name = "Games"

urlpatterns = [
    path('<slug:username>', views.GameList, name="Games"),
    path('<slug:GameID>/<slug:username>/', views.GameView, name="GamesPage"),
    path('<slug:username>/', views.AllGames, name="AllGames"),
]
