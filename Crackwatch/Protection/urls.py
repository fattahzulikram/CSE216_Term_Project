from django.urls import path, include
from . import views

app_name = "Protection"

urlpatterns = [
    path('<slug:username>', views.AllProtections, name="AllProtections"),
    path('<slug:ProtectionID>/<slug:username>', views.ProtectionView, name="ProtectionPage"),
]
