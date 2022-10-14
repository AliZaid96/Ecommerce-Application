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

class Customer(models.Model):
    phone=models.CharField(max_length=255, null=True, blank=True)
    gender=models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    Birth_date=models.DateField(null=True, blank=True)
    membership=models.CharField(max_length=1, choices=membership_choices, default="B")
    street=models.CharField(max_length=255, null=True, blank=True)
    city=models.CharField(max_length=255, null=True, blank=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name_plural = 'Customers'
