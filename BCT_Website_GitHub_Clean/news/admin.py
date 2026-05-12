from django.contrib import admin
from .models import NewsArticle, NewsCategory


def is_teamleader(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.is_staff or
            user.groups.filter(name__iexact="teamleader").exists()
        )
    )


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_add_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'status',
        'publish_date',
        'created_by',
        'is_important',
        'updated_at'
    ]
    list_filter = ['status', 'category', 'is_important', 'publish_date']
    search_fields = ['title', 'content', 'created_by__username', 'created_by__first_name', 'created_by__last_name']
    list_editable = ['is_important', 'status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'publish_date'
    
    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'content', 'category')
        }),
        ('Publication Settings', {
            'fields': ('status', 'publish_date', 'is_important')
        }),
        ('Metadata', {
            'fields': ('created_by', 'author', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_add_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)
