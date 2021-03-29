from django.db import models
from django.forms import ModelForm,Field,Form,CharField,EmailField,JSONField,ValidationError
from django.core.exceptions import ValidationError
#from django import forms
from django.contrib import messages
import uuid



def Request(registrationId):
    contact=Contact.objects.get(id=registrationId)
    person=Person.objects.get(contact=contact)
    msg={
        "id": contact.id,
        "registrationDate": contact.registrationDate,
        "locale": contact.locale,
        "person": {
            "firstName": person.firstName,
            "lastName": person.lastName,
            "email": person.email,
            "address": {
                "locale": person.address.locale,
                "addressLine1": person.address.addressLine1,
                "addressLine2": person.address.addressLine2,
                "addressLine3": person.address.addressLine3,
                "city": person.address.city,
                "state": person.address.state,
                "postcode": person.address.postcode,
                "countryIsoCode": person.address.countryIsoCode
                }
            }
        }
    try:
        organisation=Organisation.objects.get(contact=contact)
        msg["organisation"]={
            "name": organisation.name,
            "address": {
            "locale": organisation.address.locale,
            "addressLine1": organisation.address.addressLine1,
            "addressLine2": organisation.address.addressLine2,
            "addressLine3": organisation.address.addressLine3,
            "city": organisation.address.city,
            "state": organisation.address.state,
            "postcode": organisation.address.postcode,
            "countryIsoCode": organisation.address.countryIsoCode
            }
        }
    except:
        msg["organisation"]=None
    
    return msg

def Error(income):
    msg={
          "error": {
            "code": "ValidationFailed",
            "message": None
          },"fieldErrors": []}
    for error in income:
          msg["fieldErrors"].append({
              "field": error,
              "code": "IsRequired",
              "message": "The field is required"})
    return msg



class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registrationDate=models.DateTimeField(auto_now_add=True)
    locale=models.CharField(max_length=150)

    
class Person(models.Model):
    contact = models.ForeignKey('Contact',on_delete=models.CASCADE)
    firstName = models.CharField(max_length=150)
    lastName = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    address = models.ForeignKey('Address',on_delete=models.CASCADE)
    
    
class Organisation(models.Model):
    contact = models.ForeignKey('Contact',on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.ForeignKey('Address',on_delete=models.CASCADE)
    
class Address(models.Model):
    locale=models.CharField(max_length=150)
    addressLine1=models.CharField(max_length=150)
    addressLine2=models.CharField(max_length=150)
    addressLine3=models.CharField(max_length=150)
    city=models.CharField(max_length=150)
    state=models.CharField(max_length=150)
    postcode=models.CharField(max_length=150)
    countryIsoCode=models.CharField(max_length=150)




class ContactForm(Form):
    locale=CharField(required=False)
    persone=Field(required=True)
    organisation=Field(required=False)
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        super(ContactForm, self).clean()
        data=self.cleaned_data
        P_F=PersoneForm(data['persone'])
        if P_F.is_valid():
            pass
        else:
            if 'address' in P_F.errors:
                self.add_error('persone', P_F.errors['address'])
            self.add_error('persone', str(Error(P_F.errors)))
        if data['organisation'] != None:
            O_F=OrganisationForm(data['organisation'])
            if O_F.is_valid():
                pass
            else:
                self.add_error('organisation', str(Error(O_F.errors)))
    
    def save(self):
        contact_record=Contact()
        contact_record.save()
        if 'address' in self.data['persone']:
            address_data=self.data['persone'].pop('address')
            address_record=Address(**address_data)
        else:
            address_record=Address()
        address_record.save()
        self.data['persone']['address']=address_record
        self.data['persone']['contact']=contact_record
        persone_record=Person(**self.data['persone']).save()
        if 'organisation' in self.data:
            self.data['organisation']['contact']==contact_record
            address_data=self.data['organisation'].pop('address')
            address_record=Address(**address_data)
            address_record.save()
            self.data['organisation']['address']=address_record
            organisation_record=Organisation(**self.data['organisation'])
            organisation_record.save()
        return contact_record
            

class PersoneForm(Form):
    firstName=CharField(max_length=150,required=True)
    lastName=CharField(max_length=150,required=True)
    email=EmailField(max_length=254,required=True)
    address=Field(required=False)
    def __init__(self, *args, **kwargs):
        super(PersoneForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        super(PersoneForm, self).clean()
        data=self.cleaned_data
        print(data)
        if data['address'] != None:
            A_F=AddressForm(data['address'])
            if A_F.is_valid():
                pass
            else:
                print("Fail")
                print(str(Error(A_F.errors)))
                self.add_error('address', str(Error(A_F.errors)))

    
class OrganisationForm(Form):
    name=Field(required=True)
    address=Field(required=True)
    def __init__(self, *args, **kwargs):
        super(OrganisationForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        super(OrganisationForm, self).clean()
        data=self.cleaned_data
        A_F=AddressForm(data['address'])
        if A_F.is_valid():
            pass
        else:
            self.add_error('address', str(Error(A_F.errors)))
    
class AddressForm(Form):
    locale=CharField(required=False)
    addressLine1=CharField(max_length=150,required=True)
    addressLine2=CharField(max_length=150,required=False)
    addressLine3=CharField(max_length=150,required=False)
    city=CharField(max_length=40,required=False)
    state=CharField(max_length=60,required=False)
    postcode=CharField(max_length=60,required=False)
    countryIsoCode=CharField(max_length=60,required=True)












