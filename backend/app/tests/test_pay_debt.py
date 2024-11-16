import json
from app.data import schemas

def test_pay_dept(client):
    request = schemas.RequestPayDebt
    response = client.post("/pay_dept/", json.dumps(request))
    assert response.status_code == 200 
    assert response.json()["user_id"] == request.user_id or response.json() == True
