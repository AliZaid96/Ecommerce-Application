from django.shortcuts import render
from django.views import View
from .models import (
	Product,
	Categories,
	Promotion,
)

class Home(View):
	template_name = 'home.html'

	def get(self, request):
		products = Product.objects.all().order_by('title')
		products = list(products)
		categories = Categories.objects.all()

		context = {
			'title'	:	'Home',
			"products"	:	products,
			"recent_product"	:	products[:3],
			'categories'	:	categories,
		}

		return render(request , self.template_name, context)

	def post(self, request):
		# Getting sort_by filter from front-end
		sort_by = request.POST.get("order_by",False)

		# Applying sort by filter on our results
		if sort_by == 'added':
			products = Product.objects.all().order_by('-added')
		
		elif sort_by == 'unit_price':
			products = Product.objects.all().order_by('unit_price')

		else:
			products = Product.objects.all().order_by('title')

		products = list(products)
		categories = Categories.objects.all()

		context = {
			'title'	:	'Home',
			"products"	:	products,
			"recent_product"	:	products[:3],
			'categories'	:	categories,

		}

		return render(request , self.template_name, context)
