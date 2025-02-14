import pytest
import requests
import os

BASE_URL = "http://localhost:5000"

@pytest.fixture
def test_city():
    return "Paris"

def test_weather(test_city):
    response = requests.get(f"{BASE_URL}/weather?city={test_city}")
    data = response.json()
    
    assert response.status_code == 200
    assert "temperature" in data
    assert "description" in data
    assert "city" in data

def test_air_quality(test_city):
    response = requests.get(f"{BASE_URL}/air_quality?city={test_city}")
    data = response.json()

    assert response.status_code == 200
    assert "air_quality_index" in data
    assert 1 <= data["air_quality_index"] <= 5 

def test_uv_index(test_city):
    response = requests.get(f"{BASE_URL}/uv_index?city={test_city}")
    data = response.json()

    assert response.status_code == 200
    assert "uv_index" in data
    assert isinstance(data["uv_index"], (int, float))