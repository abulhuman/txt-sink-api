"""Settings for unittests."""

DEBUG = True

ALLOWED_HOSTS = ["*"]

LOGGING["formatters"]["colored"] = {  # type: ignore # noqa: F821 # pylint: disable=E0602
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
}
LOGGING["loggers"]["src"]["level"] = "DEBUG"  # type: ignore # noqa: F821 # pylint: disable=E0602
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # type: ignore # noqa: F821 # pylint: disable=E0602
LOGGING["handlers"]["console"]["formatter"] = "colored"  # type: ignore # noqa: F821 # pylint: disable=E0602

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# AWS
AWS_ACCESS_KEY_ID = "testing"
AWS_SECRET_ACCESS_KEY = "testing"
AWS_SECURITY_TOKEN = "testing"
AWS_SESSION_TOKEN = "testing"
AWS_DEFAULT_REGION = "us-east-1"
