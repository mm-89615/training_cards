__all__ = (
    "StartKb",
    "AdminKb",
    "UserKb",
    "CommonKb",
    "ChoiceActionsKb",
    "learning_words_kb",
    "get_word_kb"
)

from .inline import learning_words_kb, ChoiceActionsKb
from .reply import StartKb, AdminKb, UserKb, CommonKb, get_word_kb
