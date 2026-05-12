from django.contrib import admin
from .models import (
    SafetyInfo,
    WorkSafetyCategory,
    WorkSafetyDocument,
    WorkSafetyAcknowledgement,
    WorkSafetyEmergencyInfo,
    WorkSafetyIncidentReport
)


def is_teamleader(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.is_staff or
            user.groups.filter(name__iexact="teamleader").exists()
        )
    )


@admin.register(SafetyInfo)
class SafetyInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'updated_at']
    list_filter = ['category']
    search_fields = ['title', 'content']
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_add_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)


class WorkSafetyAcknowledgementInline(admin.TabularInline):
    model = WorkSafetyAcknowledgement
    extra = 0
    readonly_fields = ['user', 'version', 'acknowledged_at']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(WorkSafetyCategory)
class WorkSafetyCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'created_at', 'document_count']
    list_editable = ['order']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
    def document_count(self, obj):
        return obj.documents.count()
    document_count.short_description = 'Documents'
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_add_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)


@admin.register(WorkSafetyDocument)
class WorkSafetyDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'version', 'status', 'visible_to', 'updated_at', 'created_by', 'ack_count']
    list_filter = ['status', 'visible_to', 'category', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    inlines = [WorkSafetyAcknowledgementInline]
    
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'description', 'category', 'file', 'version')
        }),
        ('Visibility & Status', {
            'fields': ('status', 'visible_to')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def ack_count(self, obj):
        return obj.get_acknowledgement_count()
    ack_count.short_description = 'Acknowledged'
    
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


@admin.register(WorkSafetyAcknowledgement)
class WorkSafetyAcknowledgementAdmin(admin.ModelAdmin):
    list_display = ['document', 'user', 'version', 'acknowledged_at']
    list_filter = ['document__category', 'acknowledged_at']
    search_fields = ['document__title', 'user__username', 'user__email']
    readonly_fields = ['document', 'user', 'version', 'acknowledged_at']
    date_hierarchy = 'acknowledged_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)


@admin.register(WorkSafetyEmergencyInfo)
class WorkSafetyEmergencyInfoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'emergency_number', 'police_number', 'updated_at', 'updated_by']
    readonly_fields = ['updated_at', 'updated_by']
    
    def has_add_permission(self, request):
        return WorkSafetyEmergencyInfo.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)


@admin.register(WorkSafetyIncidentReport)
class WorkSafetyIncidentReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'occurred_at', 'submitted_by', 'status', 'created_at']
    list_filter = ['status', 'occurred_at', 'created_at']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['submitted_by', 'created_at']
    date_hierarchy = 'occurred_at'
    
    fieldsets = (
        ('Incident Information', {
            'fields': ('title', 'description', 'location', 'occurred_at')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('submitted_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_add_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)
