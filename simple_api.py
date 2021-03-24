
from flask import Flask, request,Response
import json as js
from uuid import uuid4
from datetime import datetime
from time import time

app = Flask(__name__)
app.config["DEBUG"] = True

users={}

p_fields={"person":{"firstName","lastName","email","address"},
        "organisation":{"name","address"},
        "address":{"locale","addressLine1","addressLine2","addressLine3","city","state","postcode","countryIsoCode"}}

response={
    404:{"error":{
            "code": "InternalServerError",
            "message": "Human friendly error message"
        },
        "fieldErrors": None },
    500:{"error":{
            "code": "InternalServerError",
            "message": "Human friendly error message"
        },
        "fieldErrors": None }}

res404=Response(js.dumps(response[404]), status=404, mimetype='application/json')
res500=Response(js.dumps(response[500]), status=500, mimetype='application/json')

def FieldError(fields):
    msg={
      "error": {
        "code": "ValidationFailed",
        "message": None}}
    msg["fieldErrors"]=[]
    for field in fields:
        msg["fieldErrors"].append(
            {"field": str(field),
             "code": "IsRequired",
             "message": "The field is required"})
    return Response(js.dumps(msg), status=400, mimetype='application/json')

def FieldTypeError(fields):
    msg={
      "error": {
        "code": "ValidationFailed",
        "message": None}}
    msg["FieldTypeError"]=[]
    for field in fields:
        msg["FieldTypeError"].append(
            {"field": field,
             "code": "WrongType",
             "message": "The field type is required to be dict"})
    return Response(js.dumps(msg), status=400, mimetype='application/json')

def remove_junk(data,fields_n):
    junk=data.keys()-p_fields[fields_n]
    if junk != {}:
        for i in junk:
            asd=data.pop(i)
    return data

def Registration(users,rec_data):
    u_id=str(uuid4())
    users[u_id]={}
    users[u_id]["id"]=str(u_id)
    users[u_id]["registrationDate"]=str(datetime.fromtimestamp(time()).isoformat())
    users[u_id]["locale"]="en"
    rec_data['person']=remove_junk(rec_data['person'],'person')
    rec_data['person']['address']=remove_junk(rec_data['person']['address'],'address')
    users[u_id]["person"]=rec_data['person']
    if "organisation" in rec_data:
        rec_data['organisation']=remove_junk(rec_data['organisation'],'organisation')
        rec_data['organisation']['address']=remove_junk(rec_data['organisation']['address'],'address')
        users[u_id]["organisation"]=rec_data['organisation']
    return Response(js.dumps({"registrationId": u_id}),status=201,mimetype='application/json')

def adr_valid(obj_n,adr_data):
    if type(adr_data)==dict:
        if len(adr_data)>0:
            if adr_data.keys() >={"addressLine1","countryIsoCode"}:
                return True
            else:
                fields={"addressLine1","countryIsoCode"}-adr_data.keys()
                return FieldError(fields)
        else:
            fields={f"{obj_n} 'address' addressLine1",f"{obj_n} 'address' countryIsoCode"}
            return FieldError(fields)
    else:
        return FieldTypeError({f'{obj_n} "address"'})
   
def org_valid(org_data):
    if type(org_data)==dict:
        if 'name' in org_data:
            pass
        else:
            return FieldError({'organisation "name"'})
        if 'address' in org_data:
            result = adr_valid('organisation',org_data['address'])
            print(result)
            return result
        else:
            return FieldError({'organisation "address"'})
    else:
        return FieldTypeError({'organisation'})

def validation(rec_data):
    if "person" in rec_data:
        if type(rec_data["person"])==dict:
            if rec_data["person"].keys() >= {"firstName","lastName","email"}:
                if "organisation" in rec_data:
                    result=org_valid(rec_data["organisation"])
                    if type(result) != bool:
                        return result
                if 'address' in rec_data["person"]:
                    result = adr_valid('person',rec_data["person"]["address"])
                    if type(result) != bool:
                        return result
                    else:
                        return 1
                else:
                    return 1
            else:
                field={"firstName","lastName","email"}-rec_data["person"].keys()
                return FieldError(field)
        else:
            return FieldTypeError({'persone'})
    else:
        return FieldError({"person"})
    

@app.route('/api/v1/registrations',methods=['POST'])
def Registrations():
    try:
        rec_data=js.loads(request.data)
        if 'x-correlationid' in request.headers:
            correlationid=request.headers['x-correlationid']
        result=validation(rec_data)
        if result!=1:
            return result
        else:
            result = Registration(users,rec_data)
            return result
    except:
        return res500



@app.route('/api/v1/registrations/<registrationId>',methods=['GET'])
def RegistrationRequest(registrationId):
    if 'x-correlationid' in request.headers:
        correlationid=request.headers['x-correlationid']
    if registrationId in users:
        return users[registrationId]
    else:
        return res404

app.run()

