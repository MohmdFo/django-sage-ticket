"""
FAQ Translation
"""
from modeltranslation.translator import TranslationOptions, register

from sage_ticket.models import Faq, FaqCategory


@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    """
    FAQ Translation Option
    """

    fields = (
        "question",
        "answer",
    )


@register(FaqCategory)
class FaqCategoryTranslationOptions(TranslationOptions):
    """
    FAQ Category Translation Option
    """

    fields = ("title",)
