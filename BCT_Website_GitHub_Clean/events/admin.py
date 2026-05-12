from django.contrib import admin
from .models import Event, EventParticipant


def is_teamleader(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name__iexact="TeamLeaders").exists()
        )
    )


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    extra = 0
    readonly_fields = ['created_at', 'responded_at']
    fields = ['user', 'status', 'responded_at', 'created_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'get_yes_count', 'get_no_count', 'max_participants', 'participants_visible_to', 'created_by']
    list_filter = ['date', 'participants_visible_to', 'created_at']
    search_fields = ['title', 'description', 'location']
    inlines = [EventParticipantInline]
    readonly_fields = ['created_at', 'created_by']
    
    def get_yes_count(self, obj):
        return obj.participants.filter(status='yes').count()
    get_yes_count.short_description = 'YES Count'
    
    def get_no_count(self, obj):
        return obj.participants.filter(status='no').count()
    get_no_count.short_description = 'NO Count'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_add_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'responded_at', 'created_at']
    list_filter = ['status', 'event', 'responded_at']
    search_fields = ['user__username', 'user__email', 'event__title']
    readonly_fields = ['created_at', 'responded_at']
    date_hierarchy = 'responded_at'
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_add_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)
