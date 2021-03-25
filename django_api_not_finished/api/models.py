from django.db import models
from django.forms import ModelForm
from django.core.validators import MinLengthValidator
import uuid


class Address(models.Model):
    locale=models.CharField(max_length=150)
    addressLine1=models.CharField(max_length=150, validators=[MinLengthValidator(1)])
    addressLine2=models.CharField(max_length=150)
    addressLine3=models.CharField(max_length=150)
    city=models.CharField(max_length=40)
    state=models.CharField(max_length=60)
    postcode=models.CharField(max_length=60)
    countryIsoCode=models.CharField(max_length=60, validators=[MinLengthValidator(1)])
    
    def __str__(self):
        return self.addressLine1

class Person(models.Model):
    firstName = models.CharField(max_length=150, validators=[MinLengthValidator(1)])
    lastName = models.CharField(max_length=150, validators=[MinLengthValidator(1)])
    email = models.EmailField(max_length= 254, validators=[MinLengthValidator(1)])
    address = models.ForeignKey('Address',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.firstName

class Organisation(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(1)])
    address = models.ForeignKey('Address',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registrationDate=models.DateTimeField(auto_now_add=True)
    locale=models.CharField(max_length=150)
    persone=models.ForeignKey('Person',on_delete=models.CASCADE)
    organisation=models.ForeignKey('Organisation',on_delete=models.CASCADE)


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['locale', 'addressLine1', 'addressLine2',
            'addressLine3', 'city', 'state', 'postcode','countryIsoCode']

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['firstName', 'lastName','email','address']

class OrganisationForm(ModelForm):
    class Meta:
        model = Organisation
        fields = ['name', 'address']

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['persone', 'organisation']        
