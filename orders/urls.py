from django.urls import path

from .views import place_order

app_name = "orders"

urlpatterns = [
    path("orders", place_order),
]
