#use pytest to test the api in main.py


#create a test client
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_generate_name():
    response = client.get("/generate_name")
    assert response.status_code == 200
    assert response.json()["name"] in ["Abdul", "Mohideen", "Kader", "Noor", "Iqbal"] 

import random
def test_generate_name_max_length():
    random.seed(0)
    response = client.get("/generate_name_qs?max_length=5")
    assert response.status_code == 200
    assert response.json()["name"] == "Iqbal"

def test_generate_name_stats_with():
    random.seed(0)
    response = client.get("/generate_name_qs?starts_with=M")
    assert response.status_code == 200
    assert response.json()["name"] == "Mohideen"

def test_generate_name_ax_length_stats_with():
    random.seed(0)
    response = client.get("/generate_name_qs?max_length=5&starts_with=M")
    assert response.status_code == 404

def test_generate_name_max_length_error():
    random.seed(0)
    response = client.get("/generate_name_qs?max_length=2")
    assert response.status_code == 404
