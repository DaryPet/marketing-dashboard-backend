
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from backend.campaigns.models import Campaign
from datetime import date
from django.contrib.auth.models import User

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.token_url = reverse('token_obtain_pair')
        self.protected_url = reverse('campaign-list')

    def test_obtain_token(self):
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_protected_view_without_token(self):
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'name': 'New Campaign', 'start_date': date.today(), 'end_date': date.today(), 'total_budget': 0.0}
        response = self.client.post(self.protected_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        campaign = Campaign.objects.create(name='Test Campaign', start_date=date.today(), end_date=date.today(), total_budget=0.0)
        updated_data = {'name': 'Updated Campaign', 'start_date': date.today(), 'end_date': date.today(), 'total_budget': 0.0}
        response = self.client.put(reverse('campaign-detail', kwargs={'pk': campaign.pk}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse('campaign-detail', kwargs={'pk': campaign.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_view_with_token(self):
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(self.token_url, data, format='json')
        access_token = response.data['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get(self.protected_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
