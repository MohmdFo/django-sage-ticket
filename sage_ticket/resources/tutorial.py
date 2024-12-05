from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from sage_ticket.utils.import_export.errors import DataProcessingError
from sage_ticket.utils.import_export.exclude_fields import get_language_specific_fields
from sage_ticket.models import TutorialCategory, TutorialTag, Tutorial


class TutorialResource(resources.ModelResource):

    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(TutorialCategory, "title"),
    )

    tags = fields.Field(
        column_name="tags",
        attribute="tags",
        widget=ManyToManyWidget(TutorialTag, field="title", separator=";"),
    )

    @classmethod
    def get_error_result_class(cls):
        return DataProcessingError

    class Meta:
        model = Tutorial
        base_language_fields = ["title", "summary", "description"]
        exclude = ("id",) + get_language_specific_fields(Tutorial, base_language_fields)
        import_id_fields = ("title",)
