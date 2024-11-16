from enum import Enum


class CommentType(Enum):
    Suggestion = 1
    Criticism = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ')) for key in cls]
