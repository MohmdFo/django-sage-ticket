from import_export import fields, resources

from sage_ticket.utils.import_export.errors import DataProcessingError
from sage_ticket.utils.import_export.widget import ForeignKeyNullableWidget
from sage_ticket.utils.import_export.exclude_fields import get_language_specific_fields
from sage_ticket.models import TutorialCategory


class TutorialCategoryResource(resources.ModelResource):

    @classmethod
    def get_error_result_class(cls):
        return DataProcessingError

    class Meta:
        model = TutorialCategory
        base_language_fields = ["title",]
        exclude = ("id",) + get_language_specific_fields(
            TutorialCategory,
            base_language_fields
        )
        import_id_fields = ("title",)
