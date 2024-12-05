from .attachment import AttachmentAdmin
from .comment import CommentAdmin
from .department import DepartmentAdmin
from .issue import IssueAdmin
from .faq import FaqCategoryAdmin, FaqAdmin
from .tutorial import TutorialAdmin
from .tutorial_faq import TutorialFaqAdmin
from .category import TutorialCategoryAdmin
from .tag import TutorialTagAdmin

__all__ = [
    "AttachmentAdmin",
    "CommentAdmin",
    "DepartmentAdmin",
    "IssueAdmin",
    "FaqCategoryAdmin",
    "FaqAdmin",
    "TutorialAdmin",
    "TutorialFaqAdmin",
    "TutorialCategoryAdmin",
    "TutorialTagAdmin",
]
