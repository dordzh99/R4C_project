from django.urls import path

from .views import add_robot, download_robots_in_excel

app_name = "robots"

urlpatterns = [
    path("robots", add_robot),
    path("get_robots_report", download_robots_in_excel),
]
