from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FAQ

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_faq():
    return FAQ.objects.create(
        question="What is this FAQ about?",
        answer="This is a test FAQ.",
        question_hi="यह FAQ किस बारे में है?",
        answer_hi="यह एक टेस्ट FAQ है।"
    )

@pytest.mark.django_db
class TestFAQModel:
    def test_faq_creation(self, sample_faq):
        assert FAQ.objects.count() == 1
        assert sample_faq.question == "What is this FAQ about?"

    def test_get_translated_question(self, sample_faq):
        assert sample_faq.get_question('hi') == "यह FAQ किस बारे में है?"
        assert sample_faq.get_question('en') == "What is this FAQ about?"

@pytest.mark.django_db
class TestFAQAPI:
    def test_list_faqs(self, api_client, sample_faq):
        url = reverse('faq-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_list_faqs_with_language(self, api_client, sample_faq):
        url = reverse('faq-list')
        response = api_client.get(f"{url}?lang=hi")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['question'] == "यह FAQ किस बारे में है?"

    def test_create_faq(self, api_client):
        url = reverse('faq-list')
        data = {
            'question': 'New FAQ Question',
            'answer': 'New FAQ Answer'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert FAQ.objects.count() == 1
