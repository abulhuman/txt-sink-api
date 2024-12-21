"""/files route api handler"""

from logging import Logger

import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from files.models import Files, SearchTags
from files.serializers import FileDetailSerializer, FileListSerializer

logger = Logger(__name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    region_name=settings.AWS_REGION,
    use_ssl=False,
)
s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME


@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload(request: Request) -> Response:
    """Upload a file"""
    file: UploadedFile = request.FILES.get("file")
    if not file:
        return Response({"error": "No file provided"}, status=400)

    tags = request.data.get("tags", "")

    try:
        # Read file content into a variable
        file_contents = file.read()

        # Upload the file to S3
        s3_file_name = file.name
        s3.upload_fileobj(file, s3_bucket_name, s3_file_name)

        # Retrieve the S3 object URI
        s3_object_uri = (
            f"{settings.AWS_S3_ENDPOINT_URL}/{s3_bucket_name}/{s3_file_name}"
            if settings.DEBUG else f"s3://{s3_bucket_name}/{s3_file_name}"
        )

        logger.debug("Uploaded file to S3: %s", s3_object_uri)

        file = Files(file.name, s3_object_uri, file.size, file_contents, tags)
        logger.debug("Uploading file: %s", file)
        for tag in tags.split(","):
            SearchTags(tag_name=tag, file_id=file.pk)

        return Response({"message": "File uploaded successfully", "s3_uri": s3_object_uri})

    except NoCredentialsError:
        return Response({"error": "Credentials not available"}, status=400)


@api_view(["GET"])
def get_file(_, file_id: int):
    """Get a file"""
    if not file_id:
        return Response({"error": "No file_id provided"}, status=400)
    try:
        file = Files.objects.get(id=file_id)
    except Files.DoesNotExist:
        return Response({"error": "File not found"}, status=404)
    serializer = FileDetailSerializer(file)
    return Response(serializer.data)


@api_view(["GET"])
def list_files(_):
    """List all files"""
    files = Files.objects.all()
    serializer = FileListSerializer(files, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def search_files(request: Request):
    """Search files by tags"""
    # logger.warning("[SEARCHING FILES]", request.query_params)
    print("[SEARCHING FILES]", request.query_params)
    search_by = request.query_params.get("search_by")
    if search_by == "tags":
        return search_files_by_tags(request)
    if search_by == "name":
        return search_files_by_name(request)
    if search_by == "contents":
        return search_files_by_contents(request)
    if not search_by:
        return Response(
            {"error": "No search_by parameter provided. Specify tags, name, or contents"},
            status=400,
        )
    return Response(
        {"error": "Invalid search_by parameter provided. Specify tags, name, or contents"},
        status=400,
    )


def search_files_by_tags(request: Request):
    """Search files by tags"""
    tags = request.query_params.get("tags")
    if not tags:
        return Response({"error": "No tags provided"}, status=400)

    files = Files.objects.filter(tags__contains=tags)
    # return Response({"files": files})
    serializer = FileListSerializer(files, many=True)
    return Response(serializer.data)


def search_files_by_name(request: Request):
    """Search files by name"""
    name = request.query_params.get("name")
    if not name:
        return Response({"error": "No name provided"}, status=400)

    files = Files.objects.filter(name__contains=name)
    return Response({"files": files})


def search_files_by_contents(request: Request):
    """Search files by contents"""
    contents = request.query_params.get("contents")
    if not contents:
        return Response({"error": "No contents provided"}, status=400)

    files = Files.objects.filter(contents__contains=contents)
    serializer = FileListSerializer(files, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_file(_, file_id: int):
    """Delete a file"""
    if not file_id:
        return Response({"error": "No file_id provided"}, status=400)
    try:
        file = Files.objects.get(id=file_id)
    except Files.DoesNotExist:
        return Response({"error": "File not found"}, status=404)
    file.delete()
    s3.delete_object(Bucket=s3_bucket_name, Key=file.name)
    return Response({"message": "File deleted successfully"})
