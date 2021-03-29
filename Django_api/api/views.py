from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from api.models import *



@api_view(["GET"])
def RegistrayionRequest(request,registrationId):
    try:
        msg = Request(registrationId)
        return JsonResponse(msg)
    except:
        pass
    msg={
        "error": {
            "code": "InternalServerError",
            "message": "Human friendly error message"
        },
        "fieldErrors": None
        }
    return JsonResponse(msg,status=404)

@api_view(["POST"])
def Registrayion(request):
    try:
        track_uniq_id=request.META['HTTP_X_CORELATIONID']
    except:
        pass
    C_F = ContactForm(request.data)
    if C_F.is_valid():
        contact=C_F.save()
        return JsonResponse({'registrationId':contact.id},status=201)      
    return JsonResponse(C_F.errors,status=400)

