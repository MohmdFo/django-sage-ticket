from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from sage_ticket.models import TutorialTag
from sage_ticket.resources import TutorialTagResource


@admin.register(TutorialTag)
class TutorialTagAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    """
    Django admin customization for the TutorialTag model.

    This admin class customizes the display and search capabilities for TutorialTags
    in the Django admin interface. It provides an easy-to-use interface for managing
    tags associated with blog tutorials.
    """

    resource_class = TutorialTagResource

    admin_priority = 3
    list_display = ("title", "slug", "is_published", "modified_at")
    list_filter = ("created_at", "modified_at")
    search_fields = ("title",)
    date_hierarchy = "created_at"
    save_on_top = True
    ordering = ("title",)

    fieldsets = (
        (None, {"fields": ("title", "slug", "is_published")}),
        (_("Timestamps"), {"fields": ("created_at", "modified_at")}),
    )
    readonly_fields = ("created_at", "modified_at", "slug")
