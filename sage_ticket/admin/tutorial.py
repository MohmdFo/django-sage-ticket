from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail.admin import AdminImageMixin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from sage_ticket.models import Tutorial, TutorialFaq, VideoTutorial, PictureTutorial
from sage_ticket.resources import TutorialResource


class TutorialFaqInline(TranslationTabularInline):
    model = TutorialFaq
    extra = 1


@admin.register(Tutorial)
class TutorialAdmin(
    PolymorphicParentModelAdmin,
    ImportExportModelAdmin,
    TabbedTranslationAdmin,
    AdminImageMixin
    ):
    """
    Django admin customization for the Tutorial model.

    This admin class customizes the display, search, and filter capabilities for Tutorials
    in the Django admin interface. It also provides a customized form layout for
    editing and adding new Tutorials.
    """

    resource_class = TutorialResource
    base_model = Tutorial
    show_in_index = True
    child_models = (
        PictureTutorial,
        VideoTutorial
    )

    admin_priority = 2
    inlines = (TutorialFaqInline,)
    # Display settings
    list_display = (
        "title",
        "is_published",
        "category",
        "get_tags",
        "get_summary",
        "published_at",
        "modified_at",
    )
    list_filter = ("is_published", "category", "published_at", "modified_at")
    search_fields = (
        "title",
        "slug",
        "description",
        "summary",
        "category__title",
        "tags__title",
    )
    filter_horizontal = ("tags",)
    save_on_top = True
    autocomplete_fields = (
        "author",
        "category",
        "suggested_tutorials",
        "related_tutorials",
    )
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    readonly_fields = ("created_at", "modified_at", "slug")
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "category", "is_published")},
        ),
        (
            "Content Details",
            {
                "fields": (
                    "author",
                    "summary",
                    "description",
                    "picture",
                    "banner",
                    "alternate_text",
                )
            },
        ),
        (
            _("Tags & Relationships"),
            {
                "fields": (
                    "tags",
                    "suggested_tutorials",
                    "related_tutorials",
                ),
                "classes": ("collapse",),
                "description": _(
                    "Enhance the tutorial's visibility by adding tags and "
                    "linking related tutorials."
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "published_at",
                    "modified_at",
                    "created_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @staticmethod
    @admin.display(description=_("Tags"))
    def get_tags(obj):
        return ", ".join([tag.title for tag in obj.tags.all()])

    @staticmethod
    @admin.display(description=_("Summary"))
    def get_summary(obj):
        return obj.summary if obj.summary else _("No Summary")

    # Filter customization
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("tags")
        return queryset


@admin.register(PictureTutorial)
class PictureTutorialAdmin(PolymorphicChildModelAdmin):
    """
    Django admin customization for the Tutorial model.

    This admin class customizes the display, search, and filter capabilities for Tutorials
    in the Django admin interface. It also provides a customized form layout for
    editing and adding new Tutorials.
    """
    base_model = PictureTutorial
    show_in_index = True
    readonly_fields = ("created_at", "modified_at", "slug")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "category", "is_published")},
        ),
        (
            "Content Details",
            {
                "fields": (
                    "author",
                    "summary",
                    "description",
                    "picture",
                    "banner",
                    "alternate_text",
                )
            },
        ),
        (
            _("Tags & Relationships"),
            {
                "fields": (
                    "tags",
                    "suggested_tutorials",
                    "related_tutorials",
                ),
                "classes": ("collapse",),
                "description": _(
                    "Enhance the tutorial's visibility by adding tags and "
                    "linking related tutorials."
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "published_at",
                    "modified_at",
                    "created_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(VideoTutorial)
class VideoTutorialAdmin(PolymorphicChildModelAdmin):
    """
    Django admin customization for the Tutorial model.

    This admin class customizes the display, search, and filter capabilities for Tutorials
    in the Django admin interface. It also provides a customized form layout for
    editing and adding new Tutorials.
    """
    base_model = VideoTutorial
    show_in_index = True
    readonly_fields = ("created_at", "modified_at", "slug")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "category", "is_published")},
        ),
        (
            "Content Details",
            {
                "fields": (
                    "author",
                    "summary",
                    "description",
                    "video",
                    "thumbnail",
                    "alternate_text",
                )
            },
        ),
        (
            _("Tags & Relationships"),
            {
                "fields": (
                    "tags",
                    "suggested_tutorials",
                    "related_tutorials",
                ),
                "classes": ("collapse",),
                "description": _(
                    "Enhance the tutorial's visibility by adding tags and "
                    "linking related tutorials."
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "published_at",
                    "modified_at",
                    "created_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
