from django.shortcuts import redirect, render ,HttpResponse, get_object_or_404 
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .models import (
	Customer,
	Address
)
from store.models import Categories
from .forms import (
	CustomerRegistrationForm,
	AddAddressForm,
)
from datetime import datetime

# View responsible for registering new users
class customerRegistration(View):
	template_name = "customerRegistration.html"

	def get(self , request):
		context = {
		'form'	:	CustomerRegistrationForm()
		}
		return render(request, self.template_name, context)

	def post(self, request):
		form = CustomerRegistrationForm(request.POST)
		# Checking if form is valid or it contains errors
		if form.is_valid():
			# Form is valid
			form = form.save(commit=False) # Setting form to not be saved directly as we need pk of the instance
			form.save()
			# Creating customer profile for the resitered user
			customer_obj = Customer()
			customer_obj.user = form
			customer_obj.save()
			messages.success(request,'Congratulations!! Registerion Completed')
			return redirect('home')

		return render(request, self.template_name, {"form":form})

# User responsible for rendering users profile page
def profile(request):
	# Checking if logged in user has customer profile
	try:
		customer = Customer.objects.get(user=request.user)

	except Exception as exe:
		# Logged in user doesn't have a customer profile. Creating new customr profile for the user
		customer = Customer(user=request.user)
		customer.save()

	context = {
		'customer'	:	customer,
		"categories"	:	Categories.objects.all(),
	}
	return render(request, "profile.html", context)

class UpdateProfile(View):
	template_name = 'update_profile.html'

	def get(self, request):
		current_user = request.user
		try:
			customer = Customer.objects.get(user=current_user)

		except Exception as exe:
			return redirect('home')

		context = {
<<<<<<< HEAD
			'customer'	:	customer,
			"categories"	:	Categories.objects.all(),
=======
			'customer'	:	customer
>>>>>>> main
		}
		return render(request, self.template_name, context)

	def post(self, request):
		current_user = request.user
		customer = Customer.objects.get(user=current_user)

		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		Birth_date = request.POST.get('birth_date')
		gender = request.POST.get('gender')
		Birth_date = datetime.strptime(Birth_date, '%Y-%M-%d')

		current_user.first_name = first_name
		current_user.last_name = last_name
		current_user.email = email
		current_user.save()

		customer.phone = phone
		customer.gender = gender
		customer.Birth_date = Birth_date
		customer.save()

		messages.success(request, 'Profile information updated successfully')
		return redirect('profile')

class addressBook(View):
	template_name = "address_book.html"

	def get(self,request):
		form = AddAddressForm()
		# Getting users adrress from database
		add = Address.objects.filter(user=request.user)
		context = {
			'form'	:	form,
			'add'	:	add,
			"categories"	:	Categories.objects.all(),
		}
		return render(request, self.template_name, context)

	def post(self,request):
		form = AddAddressForm(request.POST)
		user = request.user
		if form.is_valid():
			street = form.cleaned_data['street']
			city = form.cleaned_data['city']
			address_obj = Address()
			address_obj.street = street
			address_obj.city = city
			address_obj.user = user
			address_obj.save()
			messages.success(request,' Address added successfully!')

		add = Address.objects.filter(user=request.user)
		context = {
			'form'	:	form,
			'add'	:	add,
			"categories"	:	Categories.objects.all(),
		}
		return render(request, self.template_name, context)

class DeleteAddress(View):

	def get(self, request, pk):
		address = Address.objects.get(pk=pk)
		address.delete()
		messages.success(request, 'Address removed')
		return redirect('address_book')