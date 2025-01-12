from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from .models import Campaign, Channel
from decimal import Decimal
from datetime import date

class CampaignTests(TestCase):   
    # Load initial data from fixtures
    fixtures = ['backend/campaigns/fixtures/initial_data.json']

    def setUp(self):
        # Ensure that the channel exists in the database (create or get it)
        self.channel, created = Channel.objects.get_or_create(pk=1, defaults={"name": "TV", "type": "media"})
        # self.assertIsNotNone(self.channel)  # Ensure the channel exists
             
        # define  campaign data
        self.campaign_data = {
            "name": "New Sale",
            "start_date": date(2025, 1, 11),
            "end_date": date(2025, 2, 11),
            "total_budget": "5000.00",
            "spent_budget": "1000.00",
            'channels': [self.channel.id]  # Pass a list of channel IDs, not dictionaries

        }
        # Set the URL for the campaign endpoint
        self.url = reverse('campaign-list')
        
    def test_create_campaign(self):
        """Test the creation of a new campaign"""
    
        # Send a POST request to create a new campaign
        response = self.client.post(self.url, self.campaign_data, format='json')
        print(Campaign.objects.all())
        # Assert the successful creation of the campaign
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Ensure successful creation
        campaign = Campaign.objects.get(id=response.data['id'])
        self.assertEqual(campaign.name, 'New Sale')
        self.assertEqual(campaign.total_budget, Decimal('5000.00'))
        self.assertEqual(campaign.spent_budget, Decimal('1000.00'))
        self.assertEqual(campaign.channels.count(), 1)

    def test_get_campaign(self):
        """Test retrieving the list of campaigns"""
        self.client.post(self.url, self.campaign_data, format='json')  # Create a campaign first
        # Send a GET request to fetch the campaign list
        response = self.client.get(self.url)
        # Assert that the GET request is successful and returns the correct data
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure successful GET request
        self.assertEqual(len(response.data), 6)  # Ensure one campaign is returned
        # Verify the created campaign is in the response
        campaign_names = [campaign['name'] for campaign in response.data]
        self.assertIn('New Sale', campaign_names)  # Ensure 'New Sale' exists in the response

    
    def test_update_campaign(self):
        """Test updating an existing campaign"""
        # Create the campaign first
        self.client.post(self.url, self.campaign_data, format='json')
        # Define updated campaign data
        updated_data = {
            'name': 'Updated Sale',
            'start_date': date(2025, 1, 15),
            'end_date': date(2025, 1, 25),
            'total_budget': '7000.00',
            'spent_budget': '1500.00',
            'channels': [self.channel.id]
        }
        # Get the first campaign from the database
        campaign = Campaign.objects.first()
        # Send a PUT request to update the campaign
        response = self.client.put(
            reverse('campaign-detail', args=[campaign.id]),
            updated_data,
            content_type='application/json',
            format='json'
        )

        # Assert successful update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        # Define the expected response data
        expected_response = {
            'name': 'Updated Sale',
            'start_date': '2025-01-15',
            'end_date': '2025-01-25',
            'total_budget': '7000.00',
            'spent_budget': '1500.00',
            'channels': [self.channel.id]
        }
        # Remove the 'id' from the response data for comparison (because 'id' is auto-generated)
        del response.data['id'] 

        # Compare the actual response with the expected response
        self.assertDictEqual(response.data, expected_response)

        # Refresh the campaign from the database and assert the updated values
        campaign.refresh_from_db()
        self.assertEqual(campaign.name, 'Updated Sale')
        self.assertEqual(campaign.start_date, date(2025, 1, 15))
        self.assertEqual(campaign.end_date, date(2025, 1, 25))
        self.assertEqual(campaign.total_budget, Decimal('7000.00'))
        self.assertEqual(campaign.spent_budget, Decimal('1500.00'))
        self.assertEqual(list(campaign.channels.all().values_list('id', flat=True)), [self.channel.id])

    def test_delete_campaign(self):
        """Test deleting a campaign"""
        # Retrieve an existing campaign from the fixture
        campaign = Campaign.objects.first()

        # Send a DELETE request to remove this campaign
        response = self.client.delete(reverse('campaign-detail', args=[campaign.id]))
    
        # Ensure the response status is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
        # Verify that the campaign was deleted and only 4 campaigns remain (initially there were 5)
        self.assertEqual(Campaign.objects.count(), 4)


    def test_duplicate_campaign_name(self):
        """Test that duplicate campaign names are not allowed"""
        # Create a campaign first
        self.client.post(self.url, self.campaign_data, format='json')  # Create a campaign first
        
        # Attempt to create a campaign with the same name
        response = self.client.post(self.url, self.campaign_data, format='json')  # Try creating the same campaign
        
        # Assert that a validation error occurs for duplicate names
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Ensure validation error

    def test_invalid_total_budget(self):
        """Test that invalid total budget (negative value) returns an error"""
        # Modify the campaign data to set a negative total budget
        invalid_data = self.campaign_data.copy()
        invalid_data['total_budget'] = -1  # Set a negative value for total_budget
        
        # Send a POST request with the invalid data
        response = self.client.post(self.url, invalid_data, format='json')
        
        # Assert that a validation error occurs for the total budget
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Ensure validation error
        self.assertIn('Total budget must be a positive number.', str(response.data))  # Check the error message

