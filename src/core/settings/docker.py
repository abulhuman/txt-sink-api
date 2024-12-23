"""
Docker settings for the TXT_SINK_API project.

We're not serving static files for now, so we don't need WhiteNoise.
Keeping this code commented out for future reference or if we decide to serve static files.
"""
# import os

# if IN_DOCKER or os.path.isfile('/.dockerenv'):  # type: ignore # noqa: F821 # pylint: disable=E0602
#     # We need it to serve static files with DEBUG=False
#     assert MIDDLEWARE[:1] == [  # type: ignore # noqa: F821 # pylint: disable=E0602
#         'django.middleware.security.SecurityMiddleware'
#     ]
#     MIDDLEWARE.insert(1,
# 'whitenoise.middleware.WhiteNoiseMiddleware')  # type: ignore # noqa: F821 # pylint: disable=E0602
#     STORAGES = 'storages.backends.s3boto3.S3Boto3Storage'
