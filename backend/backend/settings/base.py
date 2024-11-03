from decouple import config


DEBUG = config("DEBUG", cast=bool)
