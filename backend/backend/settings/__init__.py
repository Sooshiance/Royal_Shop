from .base import DEBUG


if DEBUG:
    from .develop import *
else:
    from .production import *
