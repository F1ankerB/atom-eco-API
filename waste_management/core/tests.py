from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Organization, Storage, WasteTransfer, WasteType, StorageCapacity


class NewAPITest(APITestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Test Org", latitude=0.0, longitude=0.0
        )
        self.waste_type = WasteType.objects.create(name="bio")
        self.storage = Storage.objects.create(
            name="Test Storage", capacity=100, latitude=0.0, longitude=0.0
        )
        StorageCapacity.objects.create(
            storage=self.storage, waste_type=self.waste_type, max_capacity=100, current_capacity=0
        )

    def test_create_organization(self):
        url = reverse('organization-list-create')
        data = {
            'name': 'New Org',
            'latitude': 1.0,
            'longitude': 1.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 2)

    def test_list_organizations(self):
        url = reverse('organization-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_organization(self):
        url = reverse('organization-detail', kwargs={'pk': self.organization.pk})
        data = {
            'name': 'Updated Org',
            'latitude': 2.0,
            'longitude': 2.0
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.name, 'Updated Org')

    def test_delete_organization(self):
        url = reverse('organization-detail', kwargs={'pk': self.organization.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Organization.objects.count(), 0)

    def test_create_waste_transfer(self):
        url = reverse('waste-transfer')
        data = {
            'waste_type_id': self.waste_type.id,
            'amount': 50,
            'organization_id': self.organization.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WasteTransfer.objects.count(), 1)
