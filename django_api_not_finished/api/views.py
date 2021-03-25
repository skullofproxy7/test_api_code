from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.serializers import *
from api.models import *

@api_view(["GET"])
def Registrayion(request):
    content=Contact.objects.get()#uuid
    return JsonResponse(content)

@api_view(["POST"])
def Registrayion(request):
    track_uniq_id=request.META['HTTP_X_CORELATIONID']
    f = ContactForm(request.data)
    if f.is_valid():
        sf = f.save()
        content = {"registeredid": sf.id}
        return JsonResponse(content)
    else:
        content = {"message": "error"}
        return JsonResponse(content)
    
