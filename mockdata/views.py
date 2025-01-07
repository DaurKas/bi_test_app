from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .utils.generator import generate_receipts_dump

# Create your views here.

def send_mock_data(request):
    if request.method == 'GET':
        mock_data = generate_receipts_dump()
        return JsonResponse(mock_data, safe=False)
    
