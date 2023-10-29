from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ESGProject


class ESGProjectViewSetTest(TestCase):
    def setUp(self):
        # Create a sample ESGProject for testing
        self.project = ESGProject.objects.create(
            company_name="Test Company",
            owner_name="Test Owner",
            sector="Test Sector",
            location="Test Location",
            start_date="2023-01-01",
        )

        self.client = APIClient()

    def test_generate_report(self):
        # Get the URL for the generate_report action
        url = f'http://127.0.0.1:8000/api/v1/esg_project/{self.project.pk}/generate_report'
        print(url)

        # Send a POST request to generate the report
        response = self.client.post(url)

        # Assert that the request was successful (HTTP status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response content
        response_data = response.data
        self.assertIn("content", response_data)
        self.assertIn("name", response_data)
        self.assertIn("content_type", response_data)

    def test_generate_report_invalid_project(self):
        # Attempt to generate a report for an invalid project ID
        invalid_project_id = 999
        url = f'/api/esgprojects/{invalid_project_id}/generate_report/'

        response = self.client.post(url)

        # Assert that the request returns a not found status (HTTP status code 404)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
