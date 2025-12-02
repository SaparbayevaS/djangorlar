import pytest
from education.models import Lesson, Course
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

@pytest.fixture
def lesson(course):
    return Lesson.objects.create(title="Test Lesson", content="content", course=course)

def test_list_lessons(auth_client, cource, lesson):
    response = auth_client.get(f"/api/v1/education/courses/{course.id}/lessons/")
    assert response.status_code == 200
    assert response.data[0]["title"] == "Test lesson"

def test_create_lesson(auth_client, course):
    data = {"course": course.id, "title": "New Lesson", "content": "Content"}
    response = auth_client.post("/api/v1/education/lessons/", data, format="json")
    assert response.status_code == 201
    assert response.data["title" == "New lesson"]

def test_create_lesson_bad(auth_client):
    data = {"title": "No Course", "content": "Content"}
    response = auth_client.post("/api/v1/education/lessons/", data, format="json")
    assert response.status_code == 400
