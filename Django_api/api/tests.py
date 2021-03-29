import json
from rest_framework import status
from django.test import TestCase,Client
from django.urls import reverse

client = Client()

class APITest(TestCase):
    """ Test correct work of POST GET"""
    
    def setUp(self):
        
        self.valid_payload = {
            'locale':'en',
            'persone':{
				"firstName":"Joe",
				"email":"test@test.test",
				"lastName":"Bloggs",
				"address":{
                    "locale": "en",
                    "addressLine1": "Gateway House",
                    "addressLine2": "28 The Quadrant",
                    "addressLine3": "",
                    "city": "Richmond",
                    "state": "Surrey",
                    "postcode": "TW9 1DN",
                    "countryIsoCode": "GBR"
				}
			},
            'organisation':{
                "name": "Acme Ltd",
                "address": {
                    "locale": "en",
                    "addressLine1": "Gateway House",
                    "addressLine2": "28 The Quadrant",
                    "addressLine3": "",
                    "city": "Richmond",
                    "state": "Surrey",
                    "postcode": "TW9 1DN",
                    "countryIsoCode": "GBR"
                }
            }
		}
        
        self.invalid_payload = {
            'name': '',
            'email': 'project2@project.com',
            'score': 2,
        }
    
    
    def test_POST_valid(self):
        """Test POST valid data"""
        print("url : ",reverse('Registration'))
        response = client.post(
            reverse('Registration'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        print(response.status_code)
        print("response = ",response.json())
        self.data_id=response.json()['registrationId']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_POST_invalid(self):
        """Test POST invalid data"""
        print("url : ",reverse('Registration'))
        response = client.post(
            reverse('Registration'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        print("response code : ",response.status_code)
        print("response = ",response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_GET_invalid(self):
        """Test GET invalid UUID"""
        
        response = client.post(
            reverse('Registration'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        
        data_id=response.json()['registrationId'].replace("1","2")
        print("url : ",reverse('RegistrationRequest',args=[data_id]))
        response = client.get(
            reverse('RegistrationRequest',args=[data_id]),
            content_type='application/json'
        )
        print("response code : ",response.status_code)
        print("response = ",response.json())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_GET_valid(self):
        """Test GET valid UUID"""
        response = client.post(
            reverse('Registration'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        data_id=response.json()['registrationId']
        print("url : ",reverse('RegistrationRequest',args=[data_id]))
        response = client.get(
            reverse('RegistrationRequest',args=[data_id]),
            content_type='application/json'
        )
        print("response code : ",response.status_code)
        print("response = ",response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
