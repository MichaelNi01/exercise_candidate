import requests
import pytest
import subprocess
import time

URL = "http://127.0.0.1:5000/dogs"

VALID_DOG = {
    "breed": "Labrador",
    "age": 3,
    "name": "Buddy"
}

INVALID_DOG = {
    "breed":33,
    "age":"invalid",
    "name":"broky"
}

CONTAINER_NAME = "dogs_api_test"

@pytest.fixture(scope="session", autouse=True)
def start_container():
    image_name = "exercise:1.0"
    subprocess.run(
        [
            "podman", "run", "--name", CONTAINER_NAME, "-d", "-p", "5000:5000", image_name
        ],
        check=True
        )
    time.sleep(5)
    yield
    subprocess.run(["podman", "stop", CONTAINER_NAME], check=True)
    subprocess.run(["podman", "rm", CONTAINER_NAME], check=True)
        
@pytest.fixture
def create_dog():
    response = requests.post(URL, json=VALID_DOG)
    assert response.status_code in [200,201], f"Error: Expected status code 200 or 201, got {response.status_code}"
    id = response.json().get("id")
    data = response.json()
    yield {"id": id, "data": data,"response":response}
    requests.delete(f"{URL}/{id}")
   

def test_create_dog(create_dog):
    dog_data = create_dog["data"]
    assert dog_data["breed"] == VALID_DOG["breed"]
    assert dog_data["age"] == VALID_DOG["age"]
    assert dog_data["name"] == VALID_DOG["name"]

def test_create_invalid_dog():
    response = requests.post(URL,json=INVALID_DOG)
    assert response.status_code in [400,422]
    assert "Invalid Doggy Payload" in response.text

def test_view_valid_dog(create_dog):
    dog_id = create_dog["id"]
    response = requests.get(f"{URL}/{dog_id}")
    assert response.status_code == 200
    dog_view = response.json()
    assert dog_view["breed"] == VALID_DOG["breed"]
    assert dog_view["age"] == VALID_DOG["age"]
    assert dog_view["name"] == VALID_DOG["name"]
    
def test_delete_valid_dog(create_dog):
    dog_id = create_dog["id"]
    response = requests.delete(f"{URL}/{dog_id}")
    assert response.status_code == 200
    response = requests.get(f"{URL}/{dog_id}")
    assert response.status_code == 404
    assert "Doggo Not Found" in response.text

def test_delete_invalid_dog():
    response = requests.delete(f"{URL}/999")
    assert response.status_code == 404
    assert "Doggo Not Found" in response.text









    
    

    

