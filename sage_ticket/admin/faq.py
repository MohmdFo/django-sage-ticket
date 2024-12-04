"""
FAQ Administrators
"""
from django.contrib import admin

from modeltranslation.admin import TabbedTranslationAdmin

from sage_ticket.models import Faq, FaqCategory


class FaqInline(admin.StackedInline):
    """FAQ Inline"""

    model = Faq
    extra = 1
    fields = ("question", "answer")


@admin.register(FaqCategory)
class FaqCategoryAdmin(TabbedTranslationAdmin):
    """
    FAQ Category Admin
    """

    admin_priority = 4
    list_display = ("title", "created_at", "modified_at")
    list_filter = ("created_at", "modified_at")
    search_fields = ("title",)
    save_on_top = True
    inlines = [FaqInline]
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(Faq)
class FaqAdmin(TabbedTranslationAdmin):
    """
    FAQ Admin
    """

    admin_priority = 5
    list_display = ("question", "category", "created_at", "modified_at")
    list_filter = ("category", "created_at", "modified_at")
    search_fields = ("question", "answer", "category__title")
    list_select_related = ("category",)
    fieldsets = (
        (None, {"fields": ("question", "answer", "category")}),
        (
            "Timestamps",
            {"fields": ("created_at", "modified_at"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ("created_at", "modified_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
