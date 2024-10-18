from rest_framework import generics
from .models import Organization, Storage, WasteTransfer
from .serializers import OrganizationSerializer, StorageSerializer, WasteTransferSerializer
from django.db.models import F

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class OrganizationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class StorageListCreateView(generics.ListCreateAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

class StorageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



class WasteTransferView(APIView):

    def post(self, request, *args, **kwargs):
        waste_type_id = request.data.get('waste_type_id')
        amount = request.data.get('amount')
        organization_id = request.data.get('organization_id')

        storages = Storage.objects.filter(storagecapacity__waste_type_id=waste_type_id)
        suitable_storages = []

        for storage in storages:
            storage_capacity = storage.storagecapacity_set.filter(waste_type_id=waste_type_id).first()
            if storage_capacity:
                free_capacity = storage_capacity.max_capacity - storage_capacity.current_capacity
                if free_capacity >= amount:
                    suitable_storages.append(storage)

        if not suitable_storages:
            return Response({"detail": "Нет доступных хранилищ с нужной вместимостью."},
                            status=status.HTTP_400_BAD_REQUEST)

        nearest_storage = min(suitable_storages, key=lambda x: x.distance_to_organization(organization_id))

        waste_transfer = WasteTransfer.objects.create(
            organization_id=organization_id,
            storage=nearest_storage,
            waste_type_id=waste_type_id,
            amount=amount
        )

        storage_capacity = nearest_storage.storagecapacity_set.get(waste_type_id=waste_type_id)
        storage_capacity.current_capacity += amount
        storage_capacity.save()

        return Response(WasteTransferSerializer(waste_transfer).data, status=status.HTTP_201_CREATED)
