import json
from app.data import schemas

def test_send_code(client):
    request = schemas.RequestSendCode
    response = client.post("/code/send", json.dumps(request))
    assert response.status_code == 200 
    
def test_check_code(client):
    request = schemas.RequestCheckCode
    response = client.post("/code/check", json.dumps(request))
    assert response.status_code == 200 
    assert response.json()["status"] == True
