from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class TutorialsStatusFilter(admin.SimpleListFilter):
    title = _("Tutorials Status")
    parameter_name = "tutorials_status"

    def lookups(self, request, model_admin):
        return [
            ("no_tutorials", _("No Tutorials")),
            ("published_tutorials", _("Only With Published Tutorials")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "no_tutorials":
            return queryset.filter(tutorials__isnull=True)
        elif self.value() == "published_tutorials":
            return queryset.filter_published_tutorials().distinct()
        return queryset
