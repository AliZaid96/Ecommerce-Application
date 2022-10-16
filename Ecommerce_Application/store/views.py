from django.shortcuts import render, HttpResponse
from django.http import Http404  
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
	Product,
	Categories,
	Promotion,
)

class Home(View):
	template_name = 'home.html'

	def get(self, request):
		search_query = request.GET.get('search', None)
		print('Search Query: ',search_query)

		if search_query:
			products = Product.objects.filter(title__icontains=search_query).order_by('title')

		else:
			products = Product.objects.all().order_by('title')
		
		categories = Categories.objects.all()

		# Configuring the results for pagination
		page = request.GET.get('page', 1)
		# Add number of instances that should apear in 1 page and the queryset for the instance
		paginator = Paginator(products, 15)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)


		context = {
			'title'	:	'Home',
			"products"	:	products,
			"recent_product"	:	Product.objects.all().order_by('-added'),
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

		categories = Categories.objects.all()

		# Configuring the results for pagination
		page = request.GET.get('page', 1)
		# Add number of instances that should apear in 1 page and the queryset for the instance
		paginator = Paginator(products, 15)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)

		context = {
			'title'	:	'Home',
			"products"	:	products,
			"recent_product"	:	Product.objects.all().order_by('-added'),
			'categories'	:	categories,

		}

		return render(request , self.template_name, context)

class Category(View):
	template_name = 'home.html'

	def get(self, request, id):
		category_products = Product.objects.select_related("category").filter(category=id).order_by('title')
		categories = Categories.objects.all()

		# Configuring the results for pagination
		page = request.GET.get('page', 1)
		# Add number of instances that should apear in 1 page and the queryset for the instance
		paginator = Paginator(category_products, 15)
		try:
			category_products = paginator.page(page)
		except PageNotAnInteger:
			category_products = paginator.page(1)
		except EmptyPage:
			category_products = paginator.page(paginator.num_pages)

		context = {
			'title'	:	'Category',
			"recent_product"	:	Product.objects.select_related("category").filter(category=id).order_by('-added'),
			'categories'	:	categories,
			"products"	: 	category_products,
			"category_id"	: 	id
		}
		return render(request , self.template_name, context)

	def post(self, request, id):
		# Getting sort_by filter from front-end
		sort_by = request.POST.get("order_by",False)

		# Applying sort by filter on our results
		if sort_by == 'added':
			category_products = Product.objects.select_related("category").filter(category=id).order_by('-added')
		
		elif sort_by == 'unit_price':
			category_products = Product.objects.select_related("category").filter(category=id).order_by('unit_price')

		else:
			category_products = Product.objects.select_related("category").filter(category=id).order_by('title')

		# Configuring the results for pagination
		page = request.GET.get('page', 1)
		# Add number of instances that should apear in 1 page and the queryset for the instance
		paginator = Paginator(category_products, 15)
		try:
			category_products = paginator.page(page)
		except PageNotAnInteger:
			category_products = paginator.page(1)
		except EmptyPage:
			category_products = paginator.page(paginator.num_pages)


		context = {
			'title'	:	'Category',
			"recent_product"	:	Product.objects.select_related("category").filter(category=id).order_by('-added'),
			'categories'	:	categories,
			"products"	: 	category_products,
			"category_id"	: 	id
		}

		return render(request , self.template_name, context)

def product_detail(request, id):
	try:
		product = Product.objects.get(pk=id)

		context = {
			"product":product
		}
		return render(request,"product_detail.html",context)

	except Exception as exe:
		print('Not Found: ',exe)
		raise Http404

def error_404(request, exception):
	response.status_code = 404
	data = {
		'page'	:	'Product',
	}
	return render(request,'404.html', data)