import json
from django.shortcuts import render
from django.http.response import JsonResponse

# Create your views here.


def register(request):
    data = json.loads(request.body)
    
    return JsonResponse({
        "ok": True
    })
