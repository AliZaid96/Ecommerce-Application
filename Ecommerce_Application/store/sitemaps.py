from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Product, Order, Categories
 
 
class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.active
        
    def location(self,obj):
        return '/product/%s' % (obj.pk)

class OrderDetailSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Order.objects.all()

    def lastmod(self, obj):
        return obj.pk
        
    def location(self,obj):
        return '/order-details/%s' % (obj.pk)

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Categories.objects.all()

    def lastmod(self, obj):
        return obj.pk
        
    def location(self,obj):
        return '/category/%s' % (obj.pk)

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['contact-us']

    def location(self, item):
        return reverse(item)