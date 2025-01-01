"""RDS Database settings
    Load RDS credentials from AWS Secrets Manager"""

import json
import sys
from logging import getLogger

import boto3
from botocore.exceptions import NoCredentialsError

if not DEBUG:  # type: ignore # noqa: F821 # pylint: disable=E0602
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,  # type: ignore # noqa: F821 # pylint: disable=E0602
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,  # type: ignore # noqa: F821 # pylint: disable=E0602
        region_name=AWS_REGION,  # type: ignore # noqa: F821 # pylint: disable=E0602
    )

    aws_sm = session.client("secretsmanager",)
    logger = getLogger(__name__)
    try:
        aws_secret = aws_sm.get_secret_value(SecretId=AWS_SM_RDS_SECRET_ID)  # type: ignore # noqa: F821,E501 # pylint: disable=E0602
        secret_json = json.loads(aws_secret["SecretString"])
        MYSQL_USER = secret_json["username"]  # pylint: disable=C0103
        MYSQL_PASSWORD = secret_json["password"]  # pylint: disable=C0103
        MYSQL_HOST = secret_json["host"]  # pylint: disable=C0103
        MYSQL_PORT = secret_json["port"]  # pylint: disable=C0103
        MYSQL_DATABASE = secret_json["dbname"]  # pylint: disable=C0103
        DATABASES = {  # type: ignore # noqa: F841 # pylint: disable=[C0103,W0612]
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": MYSQL_DATABASE,
                "USER": MYSQL_USER,
                "PASSWORD": MYSQL_PASSWORD,
                "HOST": MYSQL_HOST,
                "PORT": MYSQL_PORT,
                "ATOMIC_REQUESTS": True,
                "OPTIONS": {
                    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                },
            }
        }

    except NoCredentialsError as e:
        logger.error("[Boto3] - NoCredentialsError: %s", e)
        sys.exit()
