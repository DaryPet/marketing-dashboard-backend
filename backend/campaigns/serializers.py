from rest_framework import serializers
from .models import Campaign, Channel
from datetime import datetime
from decimal import Decimal, InvalidOperation

# Serializer for the Channel model to represent channel data in JSON format
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'type']  # We expose id, name, and type of the channel

# Serializer for the Campaign model, including a nested representation of the channels
class CampaignSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)  # 'name' req
    start_date = serializers.DateField(required=True)  # 'start_date' req
    end_date = serializers.DateField(required=True)  # 'end_date' req
    total_budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)  # 'total_budget' req
    spent_budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)  # 'spent_budget' not req
    channels = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all(), many=True, required=True)  # Use PrimaryKeyRelatedField for channels

    class Meta:
        model = Campaign
        fields = ['id', 'name', 'start_date', 'end_date', 'total_budget', 'spent_budget', 'channels']

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

    # Validate that the start date is before the end date
    def validate_end_date(self, value): # Get the start date from the request data
        start_date = self.initial_data.get("start_date")
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if start_date and value < start_date:  # If end_date is before start_date, raise an error
            raise serializers.ValidationError("Start date should be before end date")
        return value
    # Check if campaign name is unique (no duplicates)
    def validate_name(self, value):
        if Campaign.objects.filter(name=value).exists(): # Check if a campaign with the same name already exists
            raise serializers.ValidationError(f"A campaign with the name '{value}' already exists.")
        return value

   

