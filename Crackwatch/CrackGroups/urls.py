from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "CrackGroups"

urlpatterns = [
    path('<slug:username>', views.AllCrackGroups, name="AllCrackGroups"),
    path('<slug:CGID>/<slug:username>', views.CGView, name="CGPage"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
