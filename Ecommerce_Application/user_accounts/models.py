from django.db import models
from django.contrib.auth.models import User

membership_choices=[
    ("B","Bronze"),
    ("S","Silver"),
    ("G","Gold")

]

gender_choices=[
    ("M","Male"),
    ("F","Female"),
    ("O","Other")

]

# Tbale to store users profile information
class Customer(models.Model):
    phone=models.CharField(max_length=255, null=True, blank=True)
    gender=models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    Birth_date=models.DateField(null=True, blank=True)
    membership=models.CharField(max_length=1, choices=membership_choices, default="B")
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.pk}'

    def get_latest_address(self):
        return Address.objects.filter(user=self.user)[0]

    class Meta:
        verbose_name_plural = 'Customers'

# Table to store users/customer adrrees
class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.street

    class Meta:
        verbose_name_plural = 'Address'
