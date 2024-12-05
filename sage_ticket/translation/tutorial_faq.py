"""
TutorialFaq Translation
"""
from modeltranslation.translator import TranslationOptions, register

from sage_ticket.models import TutorialFaq


@register(TutorialFaq)
class TutorialFaqTranslationOptions(TranslationOptions):
    """
    TutorialFaq Translation Option
    """

    fields = (
        "question",
        "answer",
    )
