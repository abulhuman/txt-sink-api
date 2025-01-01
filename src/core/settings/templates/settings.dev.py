""" Development settings """

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4#g%fqt_h=uu9bs81iy#pt0jz1rc50f*n_!x4*tl0ol!%#8lv9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "localhost:8000", "localhost:5173", "localhost:4173", "127.0.0.1"]
CORS_ALLOWED_ORIGINS = ["http://" + host for host in ALLOWED_HOSTS] + []

MYSQL_USER = "txt_sink"
MYSQL_PASSWORD = "txt_sink"
MYSQL_DATABASE = "txt_sink_db"
MYSQL_ROOT_PASSWORD = "rootpassword"
MYSQL_HOST = "127.0.0.1"

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_STORAGE_BUCKET_NAME = ""
AWS_S3_ENDPOINT_URL = "https://s3.amazonaws.com"
AWS_QUERYSTRING_AUTH = False
AWS_REGION = "us-east-1"

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None


LOGGING['formatters']['colored'] = {  # type: ignore # noqa: F821 # pylint: disable=E0602
    '()': 'colorlog.ColoredFormatter',
    'format': '%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s',
}
LOGGING['loggers']['src']['level'] = 'DEBUG'  # type: ignore # noqa: F821 # pylint: disable=E0602
LOGGING['handlers']['console']['level'] = 'DEBUG'  # type: ignore # noqa: F821 # pylint: disable=E0602
LOGGING['handlers']['console']['formatter'] = 'colored'  # type: ignore # noqa: F821 # pylint: disable=E0602
