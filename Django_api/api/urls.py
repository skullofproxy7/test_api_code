from django.urls import include, path
from . import views

urlpatterns = [
    path('v1/registration/<uuid:registrationId>', views.RegistrationRequest),
    path('v1/registration', views.Registration),
]
