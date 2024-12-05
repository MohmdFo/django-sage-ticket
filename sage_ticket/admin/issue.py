from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sage_ticket.models import Attachment, Comment, Department, Issue


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1
    fields = ("name", "extensions", "file")
    show_change_link = True


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ("title", "user", "message", "is_unread")
    show_change_link = True


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1
    fields = ("title", "description", "member")
    show_change_link = True


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline, CommentInline]
    list_display = ("subject", "state", "department", "raised_by", "is_public", "is_unread", "is_archive", "created_at")
    list_filter = ("state", "is_public", "is_unread", "is_archive", "created_at", "department")
    search_fields = ("subject", "message", "raised_by__username", "department__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "modified_at")
    autocomplete_fields = ("raised_by", "department")
    save_on_top = True

    fieldsets = (
        (
            _("Issue Details"),
            {
                "fields": ("subject", "message", "state", "severity", "department", "raised_by"),
                "description": _("Main details about the issue, including severity, state, and assignment."),
            },
        ),
        (
            _("Status"),
            {
                "fields": ("is_public", "is_unread", "is_archive"),
                "description": _("Flags indicating whether the issue is public, unread, or archived."),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "modified_at"),
                "description": _("Timestamps indicating when the issue was created and last updated."),
            },
        ),
    )
