from django.contrib import admin
from .models import Feedback, FeedbackReply

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "is_anonymous", "created_by", "created_at")
    list_filter = ("category", "status", "is_anonymous", "created_at")
    search_fields = ("title", "message", "created_by__username")

@admin.register(FeedbackReply)
class FeedbackReplyAdmin(admin.ModelAdmin):
    list_display = ("feedback", "author", "created_at")
    search_fields = ("feedback__title", "message", "author__username")
    list_filter = ("created_at",)
