from django.contrib import admin
from .models import Customer, Address

class CustomerAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'user', 'phone', 'gender', 'Birth_date', 'membership',)
	filter_list = ('gender', 'membership')

class AddressAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'user', 'city', 'street')
	filter_list = ('city',)
	filter_search = ['city']

admin.site.register(Customer, CustomerAdminTableView)
admin.site.register(Address, AddressAdminTableView)