from django.contrib import admin

from .models import Robot


class RobotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "serial",
        "model",
        "version",
        "created",
        "is_added"
    )
admin.site.register(Robot, RobotAdmin)
