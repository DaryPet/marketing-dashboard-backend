from django.db import models

# Create Сhannel model that represents an advertising channel.
class Channel(models.Model):
     # The name of the advertising channel ( "TV", "Social Media", etc.)
    name = models.CharField(max_length=100)
      
    # The type of the advertising channel ( "broadcast", "digital", "radio")
    type = models.CharField(max_length=50)

    def __str__(self):
        # Return a string representation of the Channel object (e.g., "TV (broadcast)")
        return f"{self.name} ({self.type})"

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
    
    # Many-to-many relationship with Channel model, as one campaign can use many channels
    # and each channel can be used by many campaigns.
    channels = models.ManyToManyField(Channel)

    def __str__(self):
        # Return the name of the campaign for easy identification
        return self.name
