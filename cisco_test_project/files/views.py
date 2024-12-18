from django.http import JsonResponse


def index(request):
    return JsonResponse({"hello-world":  "You're at the files index."})