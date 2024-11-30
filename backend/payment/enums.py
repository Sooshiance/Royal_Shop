from enum import Enum


class PaymentStatus(Enum):
    Paying = 1
    Paid = 2
    Failed = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ')) for key in cls]
