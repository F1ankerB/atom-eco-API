import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "waste_management.settings")
django.setup()

from core.models import WasteType, Organization, Storage, StorageCapacity

def populate_waste_types():
    waste_types = ['bio', 'glass', 'plastic']
    for code in waste_types:
        WasteType.objects.get_or_create(name=code)

def populate_organizations():
    organizations = [
        {'name': 'Org 1', 'latitude': 10.0, 'longitude': 20.0},
        {'name': 'Org 2', 'latitude': 30.0, 'longitude': 40.0}
    ]
    for org_data in organizations:
        Organization.objects.get_or_create(**org_data)

def populate_storages():
    storages = [
        {'name': 'Storage 1', 'latitude': 10.5, 'longitude': 20.5, 'capacity': 100},
        {'name': 'Storage 2', 'latitude': 30.5, 'longitude': 40.5, 'capacity': 200}
    ]
    for storage_data in storages:
        storage, _ = Storage.objects.get_or_create(name=storage_data['name'], defaults=storage_data)
        for waste_type in WasteType.objects.all():
            StorageCapacity.objects.get_or_create(
                storage=storage, waste_type=waste_type,
                defaults={'max_capacity': storage_data['capacity'], 'current_capacity': 0}
            )

if __name__ == "__main__":
    populate_waste_types()
    populate_organizations()
    populate_storages()
    print("Тестовые данные созданы!")