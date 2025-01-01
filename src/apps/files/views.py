"""/files route api handler"""

from logging import getLogger

import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.files.models import Files, SearchTags
from src.apps.files.serializers import FileDetailSerializer, FileListSerializer

logger = getLogger(__name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    region_name=settings.AWS_REGION,
)
s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME


@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload(request: Request) -> Response:
    """Upload a file"""
    file: InMemoryUploadedFile | None = request.FILES.get("file", None)
    if not file:
        return Response({"error": "No file provided"}, status=400)

    if not file.content_type == "text/plain":
        return Response({"error": "Only text('*.txt') files are allowed"}, status=400)

    file_contents = file.read()
    file_contents = file_contents.decode("utf-8")
    file_contents_char_count = len(file_contents)

    if file.size <= 512 or file_contents_char_count <= 512:
        return Response({"error": "File size should be greater than 0.5KB"}, status=400)

    if file.size >= 2048 or file_contents_char_count >= 2048:
        return Response({"error": "File size should be less than 2KB"}, status=400)

    tags = request.data.get("tags", "")

    try:
        s3_file_name = file.name
        s3.put_object(
            Bucket=s3_bucket_name,
            Key=s3_file_name,
            Body=file_contents,
            ContentType=file.content_type,
        )
        # TODO: set the `s3_object_URL` variable to the public URL of the file
        s3_object_uri = (
            f"{settings.AWS_S3_ENDPOINT_URL}/{s3_bucket_name}/{s3_file_name}"
            if settings.DEBUG else f"s3://{s3_bucket_name}/{s3_file_name}"
        )

        file = Files(
            name=file.name,
            uri=s3_object_uri,
            size=file.size,
            contents=file_contents,
            tags=tags,
        )
        file.save()
        for tag in tags.split(","):
            SearchTags(tag_name=tag, file_id=file.id).save()

        return Response(
            {
                "message": "File uploaded successfully",
                "s3_uri": s3_object_uri
            },
            status=201,
        )

    except NoCredentialsError:
        return Response({"error": "Credentials not available"}, status=500)


@api_view(["GET"])
def get_file(_, file_id: int):
    """Get a file"""
    if not file_id:
        return Response({"error": "No file_id provided"}, status=400)
    try:
        file = Files.objects.get(id=file_id)  # pylint: disable=E1101
    except Files.DoesNotExist:  # pylint: disable=E1101
        return Response({"error": "File not found"}, status=404)
    serializer = FileDetailSerializer(file)
    return Response(serializer.data)


@api_view(["GET"])
def list_files(request: Request):
    """Search files by tags"""
    search_by = request.query_params.get("search_by")
    if search_by == "tags":
        return search_files_by_tags(request)
    if search_by == "name":
        return search_files_by_name(request)
    if search_by == "contents":
        return search_files_by_contents(request)
    if not search_by:
        files = Files.objects.all()  # pylint: disable=E1101
        serializer = FileListSerializer(files, many=True)
        return Response(serializer.data)
    return Response(
        {"error": "Invalid search_by parameter provided. Specify tags, name, or contents"},
        status=400,
    )


def search_files_by_tags(request: Request):
    """Search files by tags"""
    tags = request.query_params.get("q")
    if not tags:
        return Response({"error": "No tags provided"}, status=400)

    files = Files.objects.filter(tags__contains=tags)  # pylint: disable=E1101
    serializer = FileListSerializer(files, many=True)
    return Response(serializer.data)


def search_files_by_name(request: Request):
    """Search files by name"""
    name = request.query_params.get("q")
    if not name:
        return Response({"error": "No name provided"}, status=400)

    files = Files.objects.filter(name__contains=name)  # pylint: disable=E1101
    serializer = FileListSerializer(files, many=True)
    return Response(serializer.data)


def search_files_by_contents(request: Request):
    """Search files by contents"""
    contents = request.query_params.get("q")
    if not contents:
        return Response({"error": "No contents provided"}, status=400)

    files = Files.objects.filter(contents__contains=contents)  # pylint: disable=E1101
    serializer = FileListSerializer(files, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_file(_, file_id: int):
    """Delete a file"""
    if not file_id:
        return Response({"error": "No file_id provided"}, status=400)
    try:
        file = Files.objects.get(id=file_id)  # pylint: disable=E1101
    except Files.DoesNotExist:  # pylint: disable=E1101
        return Response({"error": "File not found"}, status=404)
    file.delete()
    s3.delete_object(Bucket=s3_bucket_name, Key=file.name)
    return Response({"message": "File deleted successfully"})
