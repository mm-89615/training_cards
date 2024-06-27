__all__ = (
    "StartKb",
    "AdminKb",
    "ChoiceActionsKb",
    "learning_words_kb",
)

from .inline import learning_words_kb, ChoiceActionsKb
from .reply import StartKb, AdminKb
from .reply import start_kb, admin_kb
