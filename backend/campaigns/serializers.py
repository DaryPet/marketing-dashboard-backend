from rest_framework import serializers
from .models import Campaign, Channel

# Serializer for the Channel model to represent channel data in JSON format
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'type']  # We expose id, name, and type of the channel

# Serializer for the Campaign model, including a nested representation of the channels
class CampaignSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True)  # Include a list of channels for each campaign

    class Meta:
        model = Campaign
        fields = ['id', 'name', 'start_date', 'end_date', 'total_budget', 'spent_budget', 'channels']
