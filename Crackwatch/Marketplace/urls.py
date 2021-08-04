from django.urls import path, include
from . import views

app_name = "Marketplace"

urlpatterns = [
    path('<slug:username>', views.AllMarketplaces, name="AllMarketplaces"),
    path('<slug:MarketID>/<slug:username>', views.MarketView, name="MarketPage"),
]
