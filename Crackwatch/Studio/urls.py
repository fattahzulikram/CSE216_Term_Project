from django.urls import path, include
from . import views

app_name = "Studio"

urlpatterns = [
    path('<slug:username>', views.AllStudios, name="AllStudios"),
    path('<slug:StudioID>/<slug:username>', views.StudioView, name="StudioPage"),
]
