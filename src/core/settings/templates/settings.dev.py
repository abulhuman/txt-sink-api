# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4#g%fqt_h=uu9bs81iy#pt0jz1rc50f*n_!x4*tl0ol!%#8lv9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGGING['formatters']['colored'] = {  # type: ignore # noqa: F821
    '()': 'colorlog.ColoredFormatter',
    'format': '%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s',
}
LOGGING['loggers']['src']['level'] = 'DEBUG'  # type: ignore # noqa: F821
LOGGING['handlers']['console']['level'] = 'DEBUG'  # type: ignore # noqa: F821
LOGGING['handlers']['console']['formatter'] = 'colored'  # type: ignore # noqa: F821
