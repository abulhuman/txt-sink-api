"""Production settings"""

import os

from dotenv import load_dotenv

from . import BASE_DIR

load_dotenv(dotenv_path=str(BASE_DIR / ".production.env"), override=True)  # type: ignore # noqa: F821 # pylint: disable=E0602

SECRET_KEY = os.getenv("SECRET_KEY", os.getenv("TXT_SINK_SETTINGS_SECRET_KEY"))
DEBUG = os.getenv("DEBUG", os.getenv("TXT_SINK_SETTINGS_DEBUG")) == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", os.getenv("TXT_SINK_SETTINGS_ALLOWED_HOSTS", "")).split(",")
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", os.getenv("TXT_SINK_SETTINGS_CORS_ALLOWED_ORIGINS",
                                                                   "")).split(",")
ADMIN = os.getenv("ADMIN", os.getenv("TXT_SINK_SETTINGS_ADMIN"))

AWS_SM_RDS_SECRET_ID = os.getenv("AWS_SM_RDS_SECRET_ID", os.getenv("TXT_SINK_SETTINGS_AWS_SM_RDS_SECRET_ID"))
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", os.getenv("TXT_SINK_SETTINGS_AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", os.getenv("TXT_SINK_SETTINGS_AWS_SECRET_ACCESS_KEY"))
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", os.getenv("TXT_SINK_SETTINGS_AWS_STORAGE_BUCKET_NAME"))
