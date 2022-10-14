from django.contrib import admin
from .models import Customer

class CustomerAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'user', 'phone', 'gender', 'Birth_date', 'membership', 'city', 'street')
	filter_list = ('gender', 'membership', 'city')

admin.site.register(Customer, CustomerAdminTableView)