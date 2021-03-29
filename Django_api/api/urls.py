from django.urls import include, path
from . import views

urlpatterns = [
    path('v1/registration/<uuid:registrationId>', views.RegistrayionRequest),
    path('v1/registration/', views.Registrayion),
]