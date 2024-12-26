""" GET /health """

from logging import getLogger

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

logger = getLogger(__name__)


@api_view(["GET"])
def health(_: Request):
    """Health check endpoint"""
    logger.info("Health check")
    return Response({"status": "ok"})
