__all__ = (
    "start_kb",
    "admin_kb",
    "learning_words_kb",
    "learning_words_after_the_response_kb",
)

from .inline import start_kb, admin_kb

from .reply import learning_words_kb, learning_words_after_the_response_kb
