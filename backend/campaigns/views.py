from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from rest_framework import viewsets
from .models import Campaign
from .serializers import CampaignSerializer

# Viewset to handle the API requests for Campaigns
class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()  # Get all campaigns from the database
    serializer_class = CampaignSerializer  # Use the CampaignSerializer for data conversion
    
    # Define permissions for each action
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
        #     # Allow all users to view campaigns (GET requests)
            return [AllowAny()]
        # Only authenticated users can manage campaigns (POST, PUT, DELETE)
        return [IsAuthenticated()]
    
        
    def get_queryset(self):
        """
        Returns campaigns filtered by owner (current user) for authenticated users,
        and all campaigns for unauthenticated users (only view, no edit).
        """
        if self.request.user.is_authenticated:
            # If the user is authenticated, return only campaigns owned by the user
            return Campaign.objects.filter(owner=self.request.user)  # Only campaigns that belong to the current user
        else:
            # For unauthenticated users, return all campaigns but with read-only access
            return Campaign.objects.all() 
        
        # Create method
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
    operation_summary="List all campaigns",
    operation_description="Retrieve a list of all marketing campaigns, including associated channels.",
    responses={
        200: CampaignSerializer(many=True),
        400: "Bad Request: Invalid parameters",
        500: "Internal Server Error"
        }
)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a campaign by ID",
        operation_description="Retrieve detailed information about a specific campaign by its ID.",
        responses={
            200: CampaignSerializer,
            404: "Campaign not found: Ensure the provided ID exists in the database."
        }
    )

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
    operation_summary="Create a new campaign",
    operation_description="Add a new marketing campaign with specified details.",
    responses={
            201: CampaignSerializer,
            400: "Invalid input: Ensure all required fields are provided and valid."
        }
)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
    operation_summary="Update an existing campaign",
    operation_description="Update all fields of a marketing campaign by its ID.",
    responses={
            200: CampaignSerializer,
            400: "Invalid input: Ensure the data format is correct.",
            404: "Campaign not found: Ensure the provided ID exists in the database."
        }
)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a campaign",
        operation_description="Update specific fields of a marketing campaign by its ID.",
        responses={
            200: CampaignSerializer,
            400: "Invalid input",
            404: "Campaign not found"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
    operation_summary="Delete a campaign",
    operation_description="Remove a marketing campaign by its ID.",
    responses={
        204: "Campaign deleted successfully.",
        404: "Campaign not found: Ensure the provided ID exists in the database."
    }
)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)