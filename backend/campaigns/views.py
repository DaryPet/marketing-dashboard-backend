from django.shortcuts import render

from rest_framework import viewsets
from .models import Campaign
from .serializers import CampaignSerializer

# Viewset to handle the API requests for Campaigns
class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()  # Get all campaigns from the database
    serializer_class = CampaignSerializer  # Use the CampaignSerializer for data conversion

