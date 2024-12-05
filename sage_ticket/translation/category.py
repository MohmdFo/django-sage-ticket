"""
Tutorial Category Translation
"""
from modeltranslation.translator import TranslationOptions, register

from sage_ticket.models import TutorialCategory


@register(TutorialCategory)
class TutorialCategoryTranslationOptions(TranslationOptions):
    """
    Tutorial Category Translation Option
    """

    fields = ("title",)
