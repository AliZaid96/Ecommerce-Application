from django.contrib import admin
from .models import (
	Product,
	Categories,
	Promotion,
	Cart,
	CartItem,
	Order,
	OrderItem,
	ContactUs,
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

class CartAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'session_ID', 'customer', 'subTotal', 'created_at')

class CartItemAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'cart', 'product', 'quantity')

class OrderAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'customer', 'placed_at', 'payment_status')
	filter_list = ['payment_status']

class OrderItemAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'order', 'product', 'quantity', 'unit_price')

class ContactUsAdminTableView(admin.ModelAdmin):
	list_display = ('pk', 'name', 'email', 'phone', 'message', 'added')


admin.site.register(Product, ProductAdminTableView)
admin.site.register(Categories, CategoriesAdminTableView)
admin.site.register(Promotion, PromotionAdminTableView)
admin.site.register(Cart, CartAdminTableView)
admin.site.register(CartItem, CartItemAdminTableView)
admin.site.register(Order, OrderAdminTableView)
admin.site.register(OrderItem, OrderItemAdminTableView)
admin.site.register(ContactUs, ContactUsAdminTableView)