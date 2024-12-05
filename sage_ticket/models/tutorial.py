from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field
try:
    from sorl.thumbnail.fields import ImageField
except ImportError:
    raise ImportError(  # noqa: B904
        "Install `sorl-thumbnail` package. Run `pip install sorl-thumbnail`."
    )

try:
    import readtime
except ImportError:
    raise ImportError("Install `readtime` package. Run `pip install readtime` ")

from sage_tools.mixins.models.abstract import PictureOperationAbstract
from sage_tools.mixins.models.base import TimeStampMixin, TitleSlugDescriptionMixin

from sage_ticket.repository.manager import TutorialDataAccessLayer


class Tutorial(
    TitleSlugDescriptionMixin,
    PictureOperationAbstract,
    TimeStampMixin,
):
    """
    Represents a blog tutorial in the system.
    """

    description = CKEditor5Field(
        _("Description"),
        help_text=_(
            "Enter a detailed description of the item. This can include its purpose, "
            "characteristics, and any other relevant information."
        ),
        db_comment="Stores a detailed description of the instance.",
    )

    is_published = models.BooleanField(
        _("Is Published"),
        default=True,
        help_text=_(
            "Indicate whether this tutorial is currently published and should be displayed "
            "to all users. If unpublished, only staff users can view the tutorial."
        ),
        db_comment="Indicates if the tutorial is published (true) or hidden from non-staff users (false).",
    )

    summary = models.CharField(
        _("Summary"),
        max_length=140,
        null=True,
        blank=False,
        help_text=_("Enter a brief summary of the tutorial, up to 140 characters."),
        db_comment="A brief summary of the blog tutorial.",
    )

    picture = ImageField(
        _("Picture of Tutorial"),
        upload_to="blog/tutorials/pictures/",
        width_field="width_field",
        height_field="height_field",
        help_text=_(
            "Upload an image representing the tutorial. Ideal dimensions are [x] by [y]."
        ),
        db_comment="Image file associated with the blog tutorial.",
    )

    banner = ImageField(
        _("Banner of Tutorial Detail"),
        upload_to="blog/tutorials/banners/",
        null=True,
        blank=True,
        help_text=_(
            "Upload an image representing the tutorial. Ideal dimensions are [x] by [y]."
        ),
        db_comment="Image file associated with the blog tutorial.",
    )

    published_at = models.DateTimeField(
        _("Published At"),
        default=timezone.now,
        help_text=_("The date and time when the tutorial was published."),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tutorials",
        help_text=_("Select the author of the tutorial."),
        db_comment="References the user who authored the tutorial. Can be null if no specific author is assigned.",
    )

    tags = models.ManyToManyField(
        "TutorialTag",
        related_name="tutorials",
        verbose_name=_("Tags"),
        help_text=_("Select or add tags to categorize the tutorial."),
    )

    category = models.ForeignKey(
        "TutorialCategory",
        on_delete=models.CASCADE,
        related_name="tutorials",
        verbose_name=_("Category"),
        help_text=_("Choose the category of the tutorial."),
        db_comment="The category to which the blog tutorial belongs.",
    )

    suggested_tutorials = models.ManyToManyField(
        "self",
        verbose_name=_("Suggested tutorials"),
        blank=True,
        help_text=_("Select other tutorials to suggest alongside this product."),
    )

    related_tutorials = models.ManyToManyField(
        "self",
        verbose_name=_("Related tutorials"),
        blank=True,
        symmetrical=False,
        help_text=_("Select tutorials related to this product."),
    )

    objects: TutorialDataAccessLayer = TutorialDataAccessLayer()

    class Meta:
        """
        Meta options for the Tutorial model.

        Provides metadata and configurations for the Tutorial model such as verbose names
        and other options specific to this model.
        """

        verbose_name = _("Tutorial")
        verbose_name_plural = _("Tutorials")
        default_manager_name = "objects"
        db_table = "sage_tutorial"
        db_table_comment = "Table for preserving blog tutorials"

    @property
    def reading_time(self):
        """
        Estimate the reading time of the description using the `readtime` library.

        Returns:
            int: Estimated reading time in minutes.
        """
        result = readtime.of_text(self.description)
        # Extracting minutes from the result text (e.g., "1 min read" -> 1)
        minutes = int(
            result.text.split()[0]
        )  # assuming the format is always "X min read"
        return minutes

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        """
        Developer-friendly string representation of the Tutorial instance.

        Returns the title of the tutorial, which helps in identifying the instance when
        printed or logged, especially during debugging.
        """
        return f"<Tutorial: {self.title}>"
