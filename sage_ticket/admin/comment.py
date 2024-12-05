from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sage_ticket.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "issue", "status", "is_read", "created_at")
    list_filter = ("status", "is_read", "created_at")
    search_fields = ("title", "user__username", "issue__title")
    readonly_fields = ("created_at", "modified_at")
    ordering = ("-created_at",)

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "user", "issue", "message", "status", "is_read"),
                "description": _(
                    "Fields related to the comment, including the title, user, associated issue, message content, status, and unread status."
                ),
            },
        ),
        (
            _("Reply"),
            {
                "fields": ("replay",),
                "classes": ("collapse",),
                "description": _("Field for the reply to this comment, if any."),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "modified_at"),
                "description": _(
                    "Auto-generated timestamps indicating when the comment was created_at and last modified_at."
                ),
            },
        ),
    )
