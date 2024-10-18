from django.contrib import admin
from .models import Organization, Storage, WasteType, StorageCapacity, WasteTransfer

admin.site.register(Organization)
admin.site.register(Storage)
admin.site.register(WasteType)
admin.site.register(StorageCapacity)
admin.site.register(WasteTransfer)

