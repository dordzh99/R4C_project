from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
    )

admin.site.register(Customer, CustomerAdmin)
