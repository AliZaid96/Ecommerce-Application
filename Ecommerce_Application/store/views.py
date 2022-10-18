from django.shortcuts import render, HttpResponse
from django.http import Http404  
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
	Product,
	Categories,
	Promotion,
	Cart,
	CartItem,
	Order,
	OrderItem,
)
from user_accounts.models import Customer, Address
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

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

class CartView(View):
	template_name = 'cart.html'

	def get(self, request):
		user = request.user
		customer = Customer.objects.get(user=user)
		cart = Cart.objects.get(customer=customer)
		cartItems = CartItem.objects.filter(cart=cart)

		subTotal = 0

		for item in cartItems:
			item_total = item.get_total_price()
			subTotal = subTotal + item_total

		context = {
			"items"	:	cartItems, 
			"subTotal"	:	subTotal,
		}

		return render(request, self.template_name, context)

class CreateCart(View):
	def get(self, request):
		if request.user.is_authenticated:
			customer = Customer.objects.get(user=request.user)
			cart_obj = Cart()
			cart_obj.customer = customer
			cart_obj.save()
			return HttpResponse(cart_obj.id)

		else:
			cart_obj = Cart()
			cart_obj.save()
			return HttpResponse(cart_obj.id)

@csrf_exempt
def AddToCart(request):
	if request.method =="POST":
		customer = Customer.objects.get(user=request.user)
		print("yolo!!!!!!!!!!!!!!!!!!!!")
		cartId = request.POST.get('cartId')
		productId = request.POST.get('productId')
		quantity = request.POST.get('quantity')
		try:
			# Getting cart from database
			cart = Cart.objects.get(pk=cartId)

		except ObjectDoesNotExist:
			# creating new cart as no cart exist in the system
			cart = Cart(customer=customer)
			cart.save()

		if request.user.is_authenticated:
			customer = Customer.objects.get(user=request.user)
			cart.customer = customer
			cart.save()

		product = Product.objects.get(pk=productId)

		try:
			# Checking if product is already added to cart
			cartItem_obj = CartItem.objects.get(cart=cart, product=product)
			# Increasing products quantity based on new quantity number
			cartItem_obj.quantity = cartItem_obj.quantity + int(quantity)
			cartItem_obj.save()

		except ObjectDoesNotExist:
			# Product doesn't exist in the cart, adding new product
			cartItem_obj = CartItem()
			cartItem_obj.cart = cart
			cartItem_obj.product = product
			cartItem_obj.quantity = quantity
			cartItem_obj.save()
		messages.success(request, "Product Addred to Cart!")
		return HttpResponse("Product Added to Cart!")

def myOrders(request):
	if request.user.is_authenticated:
		user=request.user
		customer = Customer.objects.get(user=user)    
		orders = Order.objects.filter(customer=customer).order_by("-placed_at")
		add = Address.objects.filter(customer=customer)[0]

		context = {
			"orders"	:	orders,
			"add"	:	add
		}

		return render(request, "my_orders.html", context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')

def orderDetail(request,id):
	if request.user.is_authenticated:
		customer = Customer.objects.get(user=request.user)
		order = Order.objects.get(pk=id)

		order_items = OrderItem.objects.filter(order=order)
		orderItems = list(order_items)

		getcontext().prec = 2
		subTotal = Decimal(0)

		for x in orderItems:
			y=x.get_total_price()
			subTotal=subTotal+y

		add = Address.objects.filter(customer=customer)[0]
		context = {
			"items"	:	orderItems, 
			"subTotal"	:	subTotal , 
			"add"	:	add,
		}
		return render(request, "order_detail.html", context)
	
	else:
		messages.error(request, 'Please login first')
		return redirect('login')

def checkout(request):
	if request.user.is_authenticated:
		user = request.user
		customer = Customer.objects.get(user=user)
		cart = Cart.objects.get(customer=customer)
		cartItems = CartItem.objects.filter(cart=cart)

		subTotal = 0

		for item in cartItems:
			item_total = item.get_total_price()
			subTotal = subTotal + item_total

		add = Address.objects.filter(user=user)[0]

		context = {
			"items"	:	cartItems, 
			"subTotal"	:	subTotal , 
			"add"	:	add,
		}
		return render(request, "checkout.html", context)
	
	else:
		messages.error(request, 'Please login first')
		return redirect('login')

def placeOrder(request):
	if request.user.is_authenticated:
		user = request.user
		customer = Customer.objects.get(user=user)
		cart = Cart.objects.get(customer=customer)
		cartItems = CartItem.objects.filter(cart=cart)

		order = Order()
		order.customer = customer
		order.save()

		for item in cartItems:
			orderItem_obj = OrderItem(order=order, product=item.product, quantity=item.quantity, unit_price=item.product.unit_price)
			orderItem_obj.save()
		    
		cart.delete()

		context= {
			"order_id":order.id,
		}
	return render(request, "order_placed.html", context)

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
