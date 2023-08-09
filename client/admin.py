from django.contrib import admin

from .models import *


class ContactInline (admin.TabularInline):
    model = Contact
    extra = 0

class ContractorInline (admin.TabularInline):
    model = Contractor
    extra = 0

class DeliveryAddressInline (admin.TabularInline):
    model = DeliveryAddress
    extra = 0

class NoteInline (admin.TabularInline):
    model = Note
    extra = 0




class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = [ContactInline,ContractorInline,DeliveryAddressInline,NoteInline]
    list_display = ('fio',
                    'address',
                    )



admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Client, ClientAdmin)