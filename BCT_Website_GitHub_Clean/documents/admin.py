from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "visibility", "uploaded_by", "created_at")
    list_filter = ("visibility", "created_at")
    search_fields = ("title", "description")
