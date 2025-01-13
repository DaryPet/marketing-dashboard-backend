
from django.contrib import admin
from .models import Campaign, Channel

# admin for Campaign
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'total_budget', 'spent_budget')
    filter_horizontal = ('channels',) 
# admin for Channel
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')  
    search_fields = ('name', 'type')  
