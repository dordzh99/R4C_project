from django.urls import path

from .views import add_robot

app_name = "robots"

urlpatterns = [
    path("robots", add_robot),
]
