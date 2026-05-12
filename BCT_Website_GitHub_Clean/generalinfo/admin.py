from django.contrib import admin
from .models import InfoPage


def is_teamleader(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name__iexact="TeamLeaders").exists()
        )
    )


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'updated_at']
    list_filter = ['category']
    search_fields = ['title', 'content']
    list_editable = ['order']
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_add_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)

