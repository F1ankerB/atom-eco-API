from rest_framework import serializers
from .models import Organization, Storage, WasteType, StorageCapacity, WasteTransfer

class WasteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteType
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class StorageCapacitySerializer(serializers.ModelSerializer):
    waste_type = WasteTypeSerializer(read_only=True)

    class Meta:
        model = StorageCapacity
        fields = '__all__'

class StorageSerializer(serializers.ModelSerializer):
    waste_types = StorageCapacitySerializer(source='storagecapacity_set', many=True, read_only=True)

    class Meta:
        model = Storage
        fields = '__all__'

class WasteTransferSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    storage = StorageSerializer(read_only=True)
    waste_type = WasteTypeSerializer(read_only=True)

    class Meta:
        model = WasteTransfer
        fields = '__all__'