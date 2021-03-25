from django.http import JsonResponse
from rest_framework.decorators import api_view
from api.models import *

@api_view(["GET"])
def Registrayion(request):
    content=Contact.objects.get()#uuid
    return JsonResponse(content)

@api_view(["POST"])
def Registrayion(request):
    track_uniq_id=request.META['HTTP_X_CORELATIONID']
    f = ContactForm(request.POST)
    if f.is_valid():
        sf = f.save()
        content = {"registeredid": "uuid"}#uuid
        return JsonResponse(content)
    else:
        content = {"message": "error"}
        return JsonResponse(content)
    