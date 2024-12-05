from typing import ClassVar

import django_filters

from sage_ticket.models import Tutorial


class TutorialFilter(django_filters.FilterSet):
    """
    A custom filter set for the Tutorial model in a Django application.

    This filter set is designed to filter blog tutorials based on categories and tags. It
    uses django-filters, an extension to Django for creating dynamic query filters.
    `TutorialFilter` facilitates filtering the list of blog tutorials on the basis of category
    and tag slugs.
    """

    cat = django_filters.CharFilter(field_name="category", lookup_expr="slug")
    tag = django_filters.CharFilter(field_name="tags", lookup_expr="slug")

    class Meta:
        """
        Meta
        """

        model = Tutorial
        fields: ClassVar = ["cat", "tag"]
