"""
Tutorial Tag Translation
"""
from modeltranslation.translator import TranslationOptions, register

from sage_ticket.models import TutorialTag


@register(TutorialTag)
class TutorialTagTranslationOptions(TranslationOptions):
    """
    Tutorial Tag Translation Option
    """

    fields = ("title",)
