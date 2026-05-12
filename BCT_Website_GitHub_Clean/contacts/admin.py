from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name", "title", "email", "whatsapp", "is_teamleader",
        "seller_of_month_count", "icebar_of_month_count",
    )
    list_filter = ("is_teamleader",)
    search_fields = ("name", "title", "email", "whatsapp")
    list_editable = ("seller_of_month_count", "icebar_of_month_count")
