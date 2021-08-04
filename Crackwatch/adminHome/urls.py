from django.urls import path, include
from . import views

app_name = "Admin"

urlpatterns = [
    path('', views.AdminLoginView, name="AdminLogin"),
    path('<slug:user>', views.AdminHomeView, name="AdminHome"),
    path('<slug:user>/addgame/', views.AddGameView, name="AddGame"),
    path('<slug:user>/addcrackedgame/', views.AddCrackedGameView, name="AddCrackedGame"),
    path('<slug:user>/addstudio/', views.AddStudioView, name="AddStudio"),
    path('<slug:user>/addprotection/', views.AddProtectionView, name="AddProtection"),
    path('<slug:user>/addgroup/', views.AddCrackGroupView, name="AddGroup"),
    path('<slug:user>/addmarketplace/', views.AddMarketplaceView, name="AddMarketplace"),
    path('<slug:user>/createadmin/', views.CreateNewAdminView, name="CreateAdmin"),
    path('<slug:user>/addavailability/', views.AddMarketplaceToGame, name="AddAvailability"),
    path('<slug:user>/upload/', views.DemoUpload, name="DemoUpload"),
]
