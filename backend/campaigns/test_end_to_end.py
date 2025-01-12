from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Campaign, Channel
from datetime import date

class EndToEndTests(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.channel, created = Channel.objects.get_or_create(pk=1, defaults={"name": "TV", "type": "media"})
        
        # Define campaign data
        self.campaign_data = {
            "name": "End-to-End Campaign",
            "start_date": date(2025, 1, 1),
            "end_date": date(2025, 1, 31),
            "total_budget": "5000.00",
            "spent_budget": "500.00",
            "channels": [self.channel.id]
        }

        # URL for the campaign list and token obtain endpoint
        self.campaign_url = reverse('campaign-list')
        self.token_url = reverse('token_obtain_pair')
        
        # Obtain token for authentication
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(self.token_url, data, format='json')
        self.token = response.data['access']
        
    def test_create_campaign_end_to_end(self):
        """Test the full flow of creating a campaign"""
        headers = {'Authorization': f'Bearer {self.token}'}

        # Send a POST request to create a new campaign
        response = self.client.post(self.campaign_url, self.campaign_data, format='json', headers=headers)
        
        # Assert that the campaign is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify campaign data
        campaign = Campaign.objects.get(id=response.data['id'])
        self.assertEqual(campaign.name, 'End-to-End Campaign')
        self.assertEqual(campaign.total_budget, 5000.00)
        self.assertEqual(campaign.spent_budget, 500.00)
        self.assertEqual(campaign.channels.count(), 1)

    def test_get_campaign_list_end_to_end(self):
        """Test retrieving the list of campaigns"""
        headers = {'Authorization': f'Bearer {self.token}'}
        
        # Create a campaign first
        self.client.post(self.campaign_url, self.campaign_data, format='json', headers=headers)
        
        # Send a GET request to retrieve the campaign list
        response = self.client.get(self.campaign_url, headers=headers)
        
        # Assert successful retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure one campaign is returned
        self.assertEqual(response.data[0]['name'], 'End-to-End Campaign')

    def test_delete_campaign_end_to_end(self):
        """Test deleting a campaign"""
        headers = {'Authorization': f'Bearer {self.token}'}
    
        # Create a campaign first
        response = self.client.post(self.campaign_url, self.campaign_data, format='json', headers=headers)
    
        # Get the ID of the created campaign
        campaign_id = response.data['id']
    
        # Send a DELETE request to delete the campaign
        delete_url = reverse('campaign-detail', args=[campaign_id])
        response = self.client.delete(delete_url, headers=headers)
    
        # Assert that the campaign was deleted successfully (status 204)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
        # Verify the campaign is deleted from the database
        with self.assertRaises(Campaign.DoesNotExist):
            Campaign.objects.get(id=campaign_id)

    def test_update_campaign_end_to_end(self):
        """Test updating an existing campaign"""
        headers = {'Authorization': f'Bearer {self.token}'}
        
        # Create a campaign first
        response = self.client.post(self.campaign_url, self.campaign_data, format='json', headers=headers)
        
        # Define updated campaign data
        updated_data = {
            "name": "Updated End-to-End Campaign",
            "start_date": date(2025, 1, 1),
            "end_date": date(2025, 1, 31),
            "total_budget": "6000.00",
            "spent_budget": "600.00",
            "channels": [self.channel.id]
        }
        
        # Send a PUT request to update the campaign
        update_url = reverse('campaign-detail', args=[response.data['id']])
        response = self.client.put(update_url, updated_data, format='json', headers=headers)
        
        # Assert that the campaign is updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the updated campaign
        updated_campaign = Campaign.objects.get(id=response.data['id'])
        self.assertEqual(updated_campaign.name, 'Updated End-to-End Campaign')
        self.assertEqual(updated_campaign.total_budget, 6000.00)
        self.assertEqual(updated_campaign.spent_budget, 600.00)

