from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from backend.campaigns.models import Campaign, Channel

class EndToEndTests(APITestCase):

    def setUp(self):
        """Create a test user and channels for testing"""
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create test channels
        self.channel_tv = Channel.objects.create(name="TV", type="TV")
        self.channel_sm = Channel.objects.create(name="Social Media", type="Social Media")

        # Get URL for token obtain and campaign list
        self.token_url = reverse('token_obtain_pair')
        self.campaign_url = reverse('campaign-list')  # URL for fetching the list of campaigns

        # Obtain token for authenticated user
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(self.token_url, data, format='json')
        self.token = response.data['access']  # Store the access token for use in authorized requests

    def create_campaign(self):
        """Helper function to create a campaign with channels"""
        headers = {'Authorization': f'Bearer {self.token}'}  # Use the token to authenticate the request

        # Data for creating a new campaign
        campaign_data = {
            "name": "New Marketing Campaign",
            "start_date": "2025-02-01",
            "end_date": "2025-03-01",
            "total_budget": "10000",
            "spent_budget": "2000",
            "channels": [
                {"name": "TV", "type": "TV"},
                {"name": "Social Media", "type": "Social Media"}
            ]
        }

        # Send POST request to create the campaign
        response = self.client.post(self.campaign_url, campaign_data, format='json', headers=headers)
        return response  # Return the response to be used in the test

    def test_get_campaigns_for_all_users(self):
        """Test retrieving the list of campaigns for all users (both authorized and unauthorized)"""
        # Create a campaign to test with
        self.create_campaign()

        # Check if unauthenticated users can access the campaign list
        response = self.client.get(self.campaign_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure successful response (200 OK)
        self.assertGreater(len(response.data), 0)  # Ensure that some campaigns are returned

        # Check if authenticated users can access the campaign list
        headers = {'Authorization': f'Bearer {self.token}'}  # Authorization header with the token
        response = self.client.get(self.campaign_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure successful response (200 OK)
        self.assertGreater(len(response.data), 0)  # Ensure that some campaigns are returned
