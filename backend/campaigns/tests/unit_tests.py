from rest_framework.exceptions import ValidationError
from backend.campaigns.serializers import CampaignSerializer
from backend.campaigns.models import Campaign, Channel
from django.test import TestCase
from decimal import Decimal

class CampaignSerializerTest(TestCase):

    def setUp(self):
        """Setting up test data for serializer"""
        # Create channels for testing
        self.channel_tv = Channel.objects.create(name="TV", type="TV")
        self.channel_sm = Channel.objects.create(name="Social Media", type="Social Media")

        # Valid campaign data
        self.valid_campaign_data = {
            "name": "Test Campaign",
            "start_date": "2025-02-01",
            "end_date": "2025-03-01",
            "total_budget": "10000",
            "spent_budget": "2000",
            "channels": [self.channel_tv.id, self.channel_sm.id]
        }

    def test_campaign_serializer_valid_budget(self):
        """Test that the total_budget cannot be less than spent_budget"""
        valid_data = self.valid_campaign_data.copy()
        valid_data["spent_budget"] = "15000"  # Invalid spent budget

        serializer = CampaignSerializer(data=valid_data)
        self.assertFalse(serializer.is_valid())  # Should be invalid
        self.assertIn("spent_budget", serializer.errors)  # Error should be on spent_budget

    def test_campaign_serializer_invalid_budget(self):
        """Test that the serializer correctly handles invalid budget values"""
        invalid_data = self.valid_campaign_data.copy()
        invalid_data["spent_budget"] = "15000"  # Invalid spent budget

        serializer = CampaignSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # Should be invalid
        self.assertIn("spent_budget", serializer.errors)  # Error should be on spent_budget
    
    
    