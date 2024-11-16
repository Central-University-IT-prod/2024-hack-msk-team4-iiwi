import json
from app.data import schemas

def test_create_event(client):
    request = schemas.RequestEvent
    response = client.post("/event/post", json.dumps(request))
    assert response.status_code == 200 
    assert response.json()["name"] == request.name
    
def test_add_user(client):
    request = schemas.RequestAddUser
    response = client.post("/event/add_user", json.dumps(request))
    assert response.status_code == 200 
    assert response.json()["result"] == True
    
def test_get_event(client):
    request = schemas.RequestGetEvent
    response = client.post("/event/get", json.dumps(request))
    assert response.status_code == 200 
    assert response.json()["ResponseEvent"] == request.event_id
    
def test_get_all_events(client):
    request = schemas.RequestAllEvents
    response = client.post("/event/get_all", json.dumps(request))
    assert response.status_code == 200 
    assert response.json()["name"] == request.user_id
