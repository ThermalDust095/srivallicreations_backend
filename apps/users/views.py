from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def connection_status(request):
    """
    View to check the connection status.
    """
    return JsonResponse({"status": "connected"}, status=201)