from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
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
	ContactUs
)
from user_accounts.models import Customer, Address
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from datetime import datetime


stripe.api_key = 'sk_test_51LucX2CCcgV8lelJmrJ5Wt5UZC4VsC7rPaWaWigSXuHIJCvTLLTb6XovsOBiVCd8lSCvAIQ4PVL4iZlZbXKI8p0W00j41PpmDH'

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

def myOrders(request):
	user=request.user
	customer = Customer.objects.get(user=user)    
	orders = Order.objects.filter(customer=customer).order_by("-placed_at")
	print('Order: ',orders)
	add = Address.objects.filter(user=user)[0]
	print('In and loading')
	context = {
		"orders"	:	orders,
		"add"	:	add,
		"categories"	:	Categories.objects.all(),
	}
	print('In and loading')
	return render(request, 'my_orders.html', context)

def orderDetail(request,id):
	customer = Customer.objects.get(user=request.user)
	order = Order.objects.get(pk=id)

	orderItems = OrderItem.objects.filter(order=order)

	subTotal = 0

	for x in orderItems:
		y=x.get_total_price()
		subTotal=subTotal+y

	add = Address.objects.filter(user=request.user)[0]
	context = {
		"items"	:	orderItems, 
		"subTotal"	:	subTotal , 
		"add"	:	add,
		"categories"	:	Categories.objects.all(),
	}
	return render(request, "orderDetails.html", context)

class CheckoutView(View):

	def post(self, request):
		user = request.user
		customer = Customer.objects.get(user=user)
		total_items = request.POST.get('total-cart-items', None)
		subTotal = 0
		# Creating cart in database
		cart_obj = Cart()
		cart_obj.save()
		if total_items and int(total_items) > 0:
			for x in range(int(total_items)):
				product_id = request.POST.get('cart_item_number_'+str(x)+'_id')
				product_quantity = request.POST.get('cart_item_number_'+str(x)+'_quantity')
				print('Quantity: ',product_quantity)
				product = Product.objects.get(pk=product_id)
				cartItem_obj = CartItem(cart=cart_obj, product=product, quantity=product_quantity)
				cartItem_obj.save()

				subTotal = subTotal + (product.unit_price * int(product_quantity))

			cart_obj.subTotal = subTotal
			cart_obj.save()

			return redirect('confirm-order', cart_obj.session_ID)


		else:
			messages.error(request, 'No item in cart')
			return redirect('home')

class ConfirmOrderView(View):

	def get(self, request, session_ID):
		cart = Cart.objects.get(session_ID=session_ID)
		cartItems = CartItem.objects.filter(cart=cart)
		context= {
			"items"	:	cartItems,
			'subTotal'	:	cart.subTotal,
			"categories"	:	Categories.objects.all(),
			'cart_session'	:	cart.session_ID,
		}
		return render(request, "checkout.html", context)

def placeOrder(request, session_ID):
	customer = Customer.objects.get(user=request.user)
	cart_obj = Cart.objects.get(session_ID=session_ID)
	cartItem_obj = CartItem.objects.filter(cart=cart_obj)
	# Creating order
	order_obj = Order(customer=customer)
	order_obj.save()

	total_price = 0
	# Saving cart items to order
	for item in cartItem_obj:
		order_item = OrderItem(order=order_obj, product=item.product, quantity=item.quantity, unit_price=item.product.unit_price)
		order_item.save()

		total_price = total_price + (item.quantity * item.product.unit_price)

	# Saving order total
	order_obj.total_price = total_price
	order_obj.save()

	line_items_list = []

	for item in order_obj.get_items():
		line_items_list.append({
			'price': item.product.stripe_price_id,
			'quantity': item.quantity,

		})

	print('Items: ',list(line_items_list))
	
	try:
		print('Creating checkout session')
		checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			success_url = request.build_absolute_uri(reverse('order_detail', kwargs={'id': order_obj.pk})),
			cancel_url = request.build_absolute_uri(reverse('canceled', kwargs={'pk': order_obj.pk})),
			line_items= line_items_list,
			metadata = {
				'order_id':	order_obj.pk
			},
			mode="payment",
			customer_email = customer.user.email
		)
		print('Deleting cart')
		# Removing cart instance from db
		cart_obj.delete()
		# updating order status and send bill to user
		sentEmail(order_obj.pk, request.user.email)
		print('Redirecting to checout session')
		return redirect(checkout_session.url)

	except Exception as exe:
		print('Error: ',exe)
		order_obj.delete()
		return redirect('home')

def CancelOrder(request, pk):
	order_obj = Order.objects.get(id=pk)
	cart_obj = Cart.objects.get()
	order_obj.delete()
	return redirect('home')

def product_detail(request, id):
	try:
		product = Product.objects.get(pk=id)

		context = {
			"product"		:	product,
			"categories"	:	Categories.objects.all(),
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

@csrf_exempt
def stripeWebhookView(request):
	print('Inside stripe Webhook')
	payload = request.body
	sig_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None

	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
		)
	except ValueError as e:
		# Invalid payload
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		# Invalid signature
		return HttpResponse(status=400)

	# Stripe default checkout system
	if event['type'] == 'checkout.session.completed':
		
		session = event['data']['object']
		print('checkout session completed: ',session)
		customer_email = session['customer_details']['customer_email']
		order_id = session['metadata']['order_id']
		print('order_id: ',order_id)
		sentEmail(order_id, customer_email)
		
	# Custom checkout system
	elif event['type'] == 'payment_intent.succeeded':
		intent = event['data']['object']
		print('checkout intent completed: ',intent)
		customer_email = intent['customer_details']['customer_email']
		order_id = intent['metadata']['order_id']
		sentEmail(order_id, customer_email)

	elif event['type'] == 'payment_intent.created':
		print('Payment intent created')

	return HttpResponse(status=200)

def NewsletterSubscriptionView(request):
	if request.method == "POST":
		email = request.POST['EMAIL']
		from Ecommerce_Application.mailchimp_api import RegisterForNewsletter
		success = RegisterForNewsletter(email)                 # function to access mailchimp
		if success:
			messages.success(request, "Email received. Please check your email! ") # message
			print('Sending email')
			email_template = get_template('subscription_success_email.html').render()
			email_msg = EmailMessage(
				'Subscription Completed', # Subject
				email_template,
				settings.APPLICATION_EMAIL,
				[email],
				reply_to = [settings.APPLICATION_EMAIL]
			)
			email_msg.content_subtype = 'html'
			email_msg.send(fail_silently=False)
			print('Email sent')

		else:
			messages.error(request, 'Subscription Failed! Please try again letter')

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class ContactUSView(View):
	template_name = 'contact.html'

	def get(self, request):
		return render(request, 'contact.html')

	def post(self, request):
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		phone = request.POST.get('phone')
		message = request.POST.get('message')

		contact_obj = ContactUs(name=name, email=email, subject=subject, phone=phone, message=message)
		contact_obj.save()
		messages.success(request, 'Message delivered')
		return redirect('home')


# View to synx products with stripe store
def SyncDataWithStripe(request):

	stripe_products = stripe.Product.list(limit=100)
	stripe_prices = stripe.Price.list(limit=100)

	print('No of products',len(stripe_products))

	for prod in stripe_products:
		price_ = [x for x in stripe_prices.data if x.product == prod.id][0]
		price = float(price_.unit_amount / 100)
		print(price_.id)
		print(price)
		print('Getting product')
		try:
			obj = Product.objects.get(title=prod.name)
		except ObjectDoesNotExist:
			print('creating product 2')

			obj = Product(title=prod.name)
		obj.unit_price = price
		obj.stripe_price_id = price_.id
		obj.img = prod.images[0]
		obj.active = prod.active
		print('Object: ',obj)
		obj.save()

	return HttpResponse('date')

def sentEmail(order_id, user_email):
	order_obj = Order.objects.get(id=order_id)
	order_obj.payment_status = 'C'
	order_obj.save()

	context = {
		'order'	:	order_obj,
	}
	print('Sending email')
	email_template = get_template('email_receipt.html').render(context)
	email_msg = EmailMessage(
		'Bill Receipt of Your Order from E-Shop', # Subject
		email_template,
		settings.APPLICATION_EMAIL,
		[user_email],
		reply_to = [settings.APPLICATION_EMAIL]
	)
	email_msg.content_subtype = 'html'
	email_msg.send(fail_silently=False)
	print('Email sent')