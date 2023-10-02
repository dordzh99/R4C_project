from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "robot_serial",
        "customer",
        "is_waiting",
    )
admin.site.register(Order, OrderAdmin)
