from django.contrib import admin
from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "subject", "notification_type", "is_sent")
    list_filter = ("notification_type", "is_sent")
    search_fields = ("recipient", "subject", "notification_type")
    ordering = ("is_sent",)
    actions = ["mark_as_sent"]

    def mark_as_sent(self, request, queryset):
        queryset.update(is_sent=True)

    def mark_as_unsent(self, request, queryset):
        queryset.update(is_sent=False)

    mark_as_sent.short_description = "Mark selected notifications as sent"
    mark_as_unsent.short_description = "Mark selected notifications as unsent"


# Register your models here.
