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



    def test_validate_spent_budget(self):
        """Test that spent_budget cannot exceed total_budget"""
        valid_data = self.valid_campaign_data.copy()
        valid_data["spent_budget"] = "12000"  # Invalid spent budget

        serializer = CampaignSerializer(data=valid_data)
        self.assertFalse(serializer.is_valid())  # Should be invalid
        self.assertIn("spent_budget", serializer.errors)  # Error should be on spent_budget

    def test_validate_end_date(self):
        """Test that end_date should not be before start_date"""
        invalid_data = self.valid_campaign_data.copy()
        invalid_data["end_date"] = "2025-01-01"  # Invalid end date (before start date)

        serializer = CampaignSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # Should be invalid
        self.assertIn("end_date", serializer.errors)  # Error should be on end_date

    def test_validate_name_unique_for_creation(self):
        """Test that name must be unique when creating a campaign"""
        # Create an initial campaign
        Campaign.objects.create(
            name="Test Campaign",
            start_date="2025-02-01",
            end_date="2025-03-01",
            total_budget=10000,
            spent_budget=2000,
        )

        invalid_data = self.valid_campaign_data.copy()
        invalid_data["name"] = "Test Campaign"  # Duplicate name

        serializer = CampaignSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # Should be invalid
        self.assertIn("name", serializer.errors)  # Error should be on name

