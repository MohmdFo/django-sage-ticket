from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from sage_ticket.utils.import_export.errors import DataProcessingError
from sage_ticket.utils.import_export.exclude_fields import get_language_specific_fields

from sage_ticket.models import TutorialFaq, Tutorial


class TutorialFaqResource(resources.ModelResource):

    tutorial = fields.Field(
        column_name="tutorial",
        attribute="tutorial",
        widget=ForeignKeyWidget(Tutorial, "title"),
    )

    @classmethod
    def get_error_result_class(cls):
        return DataProcessingError

    class Meta:
        model = TutorialFaq
        base_language_fields = ["question", "answer"]
        exclude = ("id",) + get_language_specific_fields(
            TutorialFaq,
            base_language_fields
        )
        import_id_fields = ("question",)
