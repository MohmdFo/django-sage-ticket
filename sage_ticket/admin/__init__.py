from .attachment import AttachmentAdmin
from .comment import CommentAdmin
from .department import DepartmentAdmin
from .issue import IssueAdmin
from .faq import FaqCategoryAdmin, FaqAdmin
from .tutorial import TutorialAdmin, VideoTutorial, PictureTutorial
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
    "PictureTutorial",
    "VideoTutorial",
    "TutorialFaqAdmin",
    "TutorialCategoryAdmin",
    "TutorialTagAdmin",
]
