import pytest
from education.models import Course
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()
@pytest.fixture
def api_client():
    return APIClient

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", email="test@example.com", password="example")

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def course(user):
    return Course.objects.create(title="Test Course", description="Desc", owner=user)

def test_list_courses(auth_client, cource):
    response = auth_client.get("/api/v1/education/courses/")
    assert response.status_code == 200
    assert response.data[0]["title"] == "Test Course"

def test_create_course(auth_client):
    data = {"title": "New Course", "description": "New Desc"}
    response = auth_client.post("/api/v1/education/courses/", data, format="json")
    assert response.status_code == 201
    assert response.data["title" == "New Course"]

def test_create_course_bad(auth_client):
    data = {"desciption": "No Title"}
    response = auth_client.post("/api/v1/education/courses/", data, format="json")
    assert response.status_code == 400
