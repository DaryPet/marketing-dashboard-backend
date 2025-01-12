from django.contrib import admin

from django.contrib import admin
from .models import Campaign, Channel

# Register the Campaign and Channel models in the admin panel
admin.site.register(Campaign)
admin.site.register(Channel)

