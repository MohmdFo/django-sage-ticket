"""
FAQ Model Definition
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from sage_tools.mixins.models.base import TimeStampMixin, TitleSlugMixin


class FaqCategory(TitleSlugMixin, TimeStampMixin):
    """
    Portfolio (Gallery) category
    """

    objects = models.Manager()

    class Meta:
        """Meta Information"""

        verbose_name = _("FAQ Category")
        verbose_name_plural = _("FAQ Categories")
        db_table = "sage_ticket_faq_cat"

    def __repr__(self):
        return f"<FAQ Category: {self.title}>"


class Faq(TimeStampMixin):
    """
    FAQ Model.

    Represents a Frequently Asked Question (FAQ) entry. Each entry consists of a
    question and its corresponding answer. This model is useful for managing
    common queries that users might have, providing a quick and accessible resource
    for both site visitors and administrators.
    """

    question = models.CharField(
        _("Question"),
        max_length=150,
        help_text=_(
            "Enter the FAQ question. Keep it clear and concise to aid easy understanding."
        ),
        db_comment="The question of the FAQ. Limited to 80 characters.",
    )

    answer = models.TextField(
        _("Answer"),
        help_text=_(
            "Provide a detailed answer to the FAQ question. Aim for clarity and completeness."
        ),
        db_comment="Detailed answer to the FAQ question. Limited to 180 characters.",
    )

    category = models.ForeignKey(
        "FaqCategory",
        on_delete=models.CASCADE,
        related_name="faqs",
        verbose_name=_("Category"),
        help_text=_("Choose the category of the faq."),
        db_comment="The category to which the faq belongs.",
    )

    class Meta:
        """Meta Information"""

        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")
        db_table = "sage_ticket_faq"
        db_table_comment = "Table storing frequently asked questions and their answers for user reference."

    def __str__(self):
        """Cast to String"""
        return str(self.question)

    def __repr__(self):
        """Object Representation"""
        return f"<FAQ: {self.question}>"
