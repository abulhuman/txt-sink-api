"""RDS Database settings"""

import json
import sys
from logging import getLogger

import boto3
from botocore.exceptions import NoCredentialsError

logger = getLogger(__name__)
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,  # type: ignore # noqa: F821 # pylint: disable=E0602
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,  # type: ignore # noqa: F821 # pylint: disable=E0602
    region_name=AWS_REGION,  # type: ignore # noqa: F821 # pylint: disable=E0602
)

aws_sm = session.client("secretsmanager",)

try:
    secret = aws_sm.get_secret_value(AWS_SM_RDS_SECRET_ID)  # type: ignore # noqa: F821 # pylint: disable=E0602
    secret_json = json.loads(secret["SecretString"])
    MYSQL_USER = secret_json["username"]
    MYSQL_PASSWORD = secret_json["password"]
    MYSQL_HOST = secret_json["host"]
    MYSQL_PORT = secret_json["port"]
    MYSQL_DATABASE = secret_json["dbname"]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": MYSQL_DATABASE,
            "USER": MYSQL_USER,
            "PASSWORD": MYSQL_PASSWORD,
            "HOST": MYSQL_HOST,
            "PORT": MYSQL_PORT,
        }
    }

except NoCredentialsError as nce:
    logger.error("Error: %s", nce)
    sys.exit()
