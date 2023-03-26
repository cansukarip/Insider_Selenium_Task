import pytest
import requests
import json

BASE_URL = 'https://petstore.swagger.io/v2/pet'
added_pet_id = 0

def test_add_a_new_pet_succesfully():
    global added_pet_id  
    payload = {
        "id": 99,
        "category": {
            "id": 99,
            "name": "cansu"
        },
        "name": "namecansu",
        "photoUrls": [
            "https://www.google.com"
        ],
        "tags": [
            {
            "id": 99,
            "name": "cansu"
            }
        ],
        "status": "available"
        }    
    
    headers = {'Content-Type': 'application/json', 'accept': 'application/json' } 
    response = requests.request("POST", BASE_URL, headers=headers, data=json.dumps(payload))     
    assert response.status_code == 200
    json_response = json.loads(response.text)
    added_pet_id = json_response["id"]    

def test_update_existing_pet_by_petId_successfully():
    global added_pet_id  
    payload = {
        "id": added_pet_id,
        "category": {
            "id": 99,
            "name": "cansu"
        },
        "name": "nameupdated",
        "photoUrls": [
            "https://www.google.com"
        ],
        "tags": [
            {
            "id": 99,
            "name": "cansu"
            }
        ],
        "status": "available"
        }    
    
    headers = {'Content-Type': 'application/json', 'accept': 'application/json' } 
    response = requests.request("PUT", BASE_URL, headers=headers, data=json.dumps(payload))     
    assert response.status_code == 200
    json_response = json.loads(response.text)
    assert json_response["name"] == "nameupdated"

def test_get_pet_by_petId_successfully():
    global added_pet_id
    URL = BASE_URL + "/" + str(added_pet_id)
    headers = {'Content-Type': 'application/json'} 
    response = requests.request("GET", URL, headers=headers)    
    assert response.status_code == 200
    print(response.text)

def test_get_pet_by_wrong_petId():
    URL = BASE_URL + "/0"
    headers = {'Content-Type': 'application/json'} 
    response = requests.request("GET", URL, headers=headers)    
    assert response.status_code == 404
    print(response.text)

def test_get_available_pet_by_status():
    URL = BASE_URL + "/findByStatus?status=available"
    headers = {'Content-Type': 'application/json'} 
    response = requests.request("GET", URL, headers=headers)    
    assert response.status_code == 200

def test_get_pending_pet_by_status():
    URL = BASE_URL + "/findByStatus?status=pending"
    headers = {'Content-Type': 'application/json'} 
    response = requests.request("GET", URL, headers=headers)    
    assert response.status_code == 200

def test_get_sold_pet_by_status():
    URL = BASE_URL + "/findByStatus?status=sold"
    headers = {'Content-Type': 'application/json'} 
    response = requests.request("GET", URL, headers=headers)    
    assert response.status_code == 200

def test_update_existing_pet_by_form_data_successfully():
    global added_pet_id
    URL = BASE_URL + "/" + str(added_pet_id)
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
    form_data = {        
        "name": "newupdatedname",
        "status" : "sold"
    } 
    response = requests.request("POST", URL, headers=headers, data=form_data)     
    assert response.status_code == 200      
    
def test_delete_existing_pet_by_petId_successfully():
    global added_pet_id
    URL = BASE_URL + "/" + str(added_pet_id)
    headers = {'Content-Type': 'application/json'} 
    response = requests.request("DELETE", URL, headers=headers)    
    assert response.status_code == 200