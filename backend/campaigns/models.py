from django.db import models
from django.contrib.auth import get_user_model

# Create Сhannel model that represents an advertising channel.from django.db import models
class Channel(models.Model):
    # Defining a ChannelType enum with predefined choices
    class ChannelType(models.TextChoices):
        TV = 'TV', 'Television'
        SOCIAL_MEDIA = 'Social Media', 'Social Networks'
        RADIO = 'Radio', 'Radio'
        SEARCH_ENGINE = 'Search Engine', 'Search Engines'

    # The 'name' field will be a choice from the predefined list in ChannelType
    name = models.CharField(
        max_length=50,  # Limiting the length of the string for the name
        choices=ChannelType.choices,  # Limiting the choices to the ones defined in ChannelType
    )
    
    # The 'type' field will also be a choice from the predefined list in ChannelType
    type = models.CharField(
        max_length=50,
        choices=ChannelType.choices,  # Limiting the choices to the ones defined in ChannelType
    )

    def __str__(self):
        # String representation of the Channel object, displaying the readable type and name
        return f"{self.get_name_display()} ({self.get_type_display()})"


class Campaign(models.Model):
    # Name of the marketing campaign ( "Summer Sale", "Brand Awareness")
    name = models.CharField(max_length=200)
    
    # Start date of the campaign
    start_date = models.DateField()
    
    # End date of the campaign
    end_date = models.DateField()
    
    # Total allocated budget for the campaign
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Amount of the budget that has been spent so far (defaults to 0)
    spent_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="campaigns")

    # Many-to-many relationship with Channel model, as one campaign can use many channels
    # and each channel can be used by many campaigns.
    channels = models.ManyToManyField(Channel)

    def __str__(self):
        # Return the name of the campaign for easy identification
        return self.name
