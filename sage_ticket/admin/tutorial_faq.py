"""
FAQ Administrators
"""

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from sage_ticket.models import TutorialFaq
from sage_ticket.resources import TutorialFaqResource


@admin.register(TutorialFaq)
class TutorialFaqAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    """
    FAQ Admin
    """

    resource_class = TutorialFaqResource

    admin_priority = 5
    list_display = ("question", "tutorial", "created_at", "modified_at")
    list_filter = ("created_at", "modified_at")
    search_fields = ("question", "answer", "tutorial__title")
    list_select_related = ("tutorial",)
    autocomplete_fields = ("tutorial",)
    fieldsets = (
        (None, {"fields": ("question", "answer", "tutorial")}),
        (
            "Timestamps",
            {"fields": ("created_at", "modified_at"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ("created_at", "modified_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
