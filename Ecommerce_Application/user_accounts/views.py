from django.shortcuts import redirect, render ,HttpResponse, get_object_or_404 
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .models import (
	Customer
)
from .forms import (
	CustomerRegistrationForm
)

class customerRegistration(View):
	template_name = "customerRegistration.html"
	def get(self , request):
		context = {
		'form'	:	CustomerRegistrationForm()
		}
		return render(request, self.template_name, context)

	def post(self, request):
		form = CustomerRegistrationForm(request.POST)

		if form.is_valid():
			form = form.save(commit=False)
			form.save()
			customer_obj = Customer()
			customer_obj.user = form
			customer_obj.save()
			messages.success(request,'Congratulations!! Registerion Completed')
			return redirect('home')

		return render(request, self.template_name, {"form":form})
