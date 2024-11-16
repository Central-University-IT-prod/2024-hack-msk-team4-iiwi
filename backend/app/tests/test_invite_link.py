import json
from app.data import schemas

def test_generate_invite_link(client):
    request = schemas.RequestInviteLink
    response = client.post("/invite_link/generate", json.dumps(request))
    assert response.status_code == 200 
    assert response.json()["link"] == request.event_id

def test_check_invite_link(client):
    request = {"user": "Anton"}
    response = client.post("/invite_link/check/{short_link}", json.dumps(request))
    assert response.status_code == 200
