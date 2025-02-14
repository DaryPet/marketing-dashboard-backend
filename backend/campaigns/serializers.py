
from rest_framework import serializers
from .models import Campaign, Channel
from datetime import datetime
from decimal import Decimal, InvalidOperation

# Serializer for the Channel model to represent channel data in JSON format
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', 'type']  # Expose 'name' and 'type' of the channel

# Serializer for the Campaign model, including a nested representation of the channels
class CampaignSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)  # 'name' required
    start_date = serializers.DateField(required=True)  # 'start_date' required
    end_date = serializers.DateField(required=True)  # 'end_date' required
    total_budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)  # 'total_budget' required
    spent_budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)  # 'spent_budget' not required
    channels = ChannelSerializer(many=True)  # Nested ChannelSerializer
    # channels = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all(), many=True)

    class Meta:
        model = Campaign
        fields = ['id', 'name', 'start_date', 'end_date', 'total_budget', 'spent_budget', 'channels', 'owner_id']

    def validate_total_budget(self, value):
        try:
            value = Decimal(value)
        except (TypeError, ValueError, InvalidOperation):
            raise serializers.ValidationError("Total budget must be a valid number.")
        if value <= 0:
            raise serializers.ValidationError("Total budget must be a positive number.")
        return value

    def validate_spent_budget(self, value):
        try:
            value = Decimal(value)
        except (TypeError, ValueError, InvalidOperation):
            raise serializers.ValidationError("Spent budget must be a valid number.")
        total_budget = self.initial_data.get('total_budget')
        if total_budget:
            total_budget = Decimal(total_budget)
            if value > total_budget:
                raise serializers.ValidationError("Spent budget cannot exceed total budget.")
        return value

    def validate_end_date(self, value):
        start_date = self.initial_data.get("start_date")
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if start_date and value < start_date:
            raise serializers.ValidationError("Start date should be before end date")
        return value
    # Validate name (Only for creation, not for update)
    def validate_name(self, value):
        # Check only if it is a new record (no instance)
        if not self.instance:   # If this is a creation (no instance)
            if Campaign.objects.filter(name=value).exists():
                raise serializers.ValidationError(f"A campaign with the name '{value}' already exists.")
        return value

    #     return campaign
    def create(self, validated_data):
        # Extracting the 'channels' data from the validated input.
        channels_data = validated_data.pop('channels')  # Remove 'channels' from validated_data

        # Creating a new Campaign instance using the remaining validated data.
        campaign = Campaign.objects.create(**validated_data)  # Create a new campaign

        # Loop through the channels data to associate each channel with the new campaign.
        for channel_data in channels_data:  # For each channel in the 'channels' data

            # Search for an existing channel with the same name and type.
            # If no such channel exists, create a new one.
            channel, created = Channel.objects.get_or_create(
                name=channel_data['name'], 
                type=channel_data['type']
            )
        
            # Add the found (or created) channel to the campaign's many-to-many relationship.
            campaign.channels.add(channel)  # Add the channel to the 'channels' many-to-many relationship of the campaign.

        # Return the newly created campaign instance.
        return campaign  # Return the newly created campaign with associated channels.

    def update(self, instance, validated_data):
        print(f"Validated data: {validated_data}") 
        # Update campaign fields
        instance.name = validated_data.get('name', instance.name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.total_budget = validated_data.get('total_budget', instance.total_budget)
        instance.spent_budget = validated_data.get('spent_budget', instance.spent_budget)

        # Process channel updates
        channels_data = validated_data.get('channels', [])
        instance.channels.clear()  # Clear old channels

        for channel_data in channels_data:
            # Get channels by name and type
            channels = Channel.objects.filter(name=channel_data['name'], type=channel_data['type'])
        
            if channels.exists():
                # Add the channel(s) to the campaign (if at least one is found)
                instance.channels.add(*channels)
            else:
                raise serializers.ValidationError(f"Channel with name {channel_data['name']} and type {channel_data['type']} does not exist.")

        instance.save()
        return instance
