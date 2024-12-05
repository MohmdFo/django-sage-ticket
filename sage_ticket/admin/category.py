from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from sage_ticket.admin.filters import TutorialsStatusFilter
from sage_ticket.models import TutorialCategory
from sage_ticket.resources import TutorialCategoryResource


@admin.register(TutorialCategory)
class TutorialCategoryAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    """
    Django admin customization for the TutorialCategory model.

    This admin class customizes the display and search capabilities for TutorialCategories
    in the Django admin interface. It provides an intuitive interface for managing blog
    tutorial categories.
    """

    resource_class = TutorialCategoryResource

    # Display settings
    admin_priority = 1
    list_display = (
        "title",
        "slug",
        "is_published",
        "published_tutorials_count",
        "modified_at",
    )
    list_filter = (TutorialsStatusFilter, "is_published")
    search_fields = ("title",)
    date_hierarchy = "created_at"
    ordering = ("title",)
    save_on_top = True

    # Form layout customization
    fieldsets = (
        (None, {"fields": ("title", "slug", "is_published")}),
        (_("Timestamps"), {"fields": ("created_at", "modified_at")}),
    )
    readonly_fields = ("created_at", "modified_at", "slug")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.join_tutorials()
        return queryset

    @admin.display(description=_("Published Tutorials"))
    def published_tutorials_count(self, obj):
        # Annotate the count of published tutorials directly when accessed
        return obj.tutorials.filter(is_published=True).count()
