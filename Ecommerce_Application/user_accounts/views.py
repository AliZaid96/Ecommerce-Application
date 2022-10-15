from django.shortcuts import redirect, render ,HttpResponse, get_object_or_404 
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .models import (
	Customer,
	Address
)
from .forms import (
	CustomerRegistrationForm,
	AddAddressForm,
)

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

	context = {
		'customer'	:	customer
	}
	return render(request, "profile.html", context)

class addressBook(View):
	template_name = "address_book.html"

	def get(self,request):
		form = AddAddressForm()
		# Getting users adrress from database
		add = Address.objects.filter(user=request.user)
		context = {
			'form'	:	form,
			'add'	:	add,
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
		}
		return render(request, self.template_name, context)

