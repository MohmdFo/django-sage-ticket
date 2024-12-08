"""
Tutorial Category Translation
"""
from modeltranslation.translator import TranslationOptions, register

from sage_ticket.models import Tutorial


@register(Tutorial)
class TutorialTranslationOptions(TranslationOptions):
    """
    Tutorial Category Translation Option
    """

    fields = ("title", "description", "summary")
