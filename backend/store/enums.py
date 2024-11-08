from enum import Enum


class Share(Enum):
    Golden = 1
    Silver = 2
    Bronze = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ')) for key in cls]


class OrderStatus(Enum):
    Pending = 1
    Shipped = 2
    Delivered = 3
    Cancelled = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ')) for key in cls]
