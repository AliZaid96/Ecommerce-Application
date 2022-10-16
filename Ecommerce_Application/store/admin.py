from django.contrib import admin
from .models import (
	Product,
	Categories,
	Promotion
)

class ProductAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'title', 'description', 'unit_price', 'inventory', 'added', 'last_update', 'category', 'img')
	filter_list = ('added', 'last_update', 'category')
	filter_search = ['title']

class CategoriesAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'title', 'featured_product')
	filter_search = ['title']

class PromotionAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'description', 'discount')
	filter_search = ['description']

admin.site.register(Product, ProductAdminTableView)
admin.site.register(Categories, CategoriesAdminTableView)
admin.site.register(Promotion, PromotionAdminTableView)