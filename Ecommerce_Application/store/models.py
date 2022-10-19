from django.db import models
import datetime
import os
from user_accounts.models import Customer
import uuid

payment_status_choices = [
    ("P", "Pending"),
    ("C", "Complete"),
    ("F", "Failed")
]

gender_choices=[
    ("M","Male"),
    ("F","Female"),
    ("O","Other")

]

def filepath(request,filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (current_time,old_name)
    return os.path.join("uploads/",filename)

# Models to store categories for product
class Categories(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True ,blank=True, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

# Model to store promotions for the product
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = 'Promotions'

# Model to store products information
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2 )
    inventory = models.IntegerField()
    added = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    promotion = models.ManyToManyField(Promotion, blank=True)
    img = models.ImageField(upload_to=filepath, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Products'

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    session_ID = models.CharField(max_length=50, default=uuid.uuid4)
    subTotal = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Carts'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.quantity * self.product.unit_price

    class Meta:
        verbose_name_plural = 'Cart Items'

class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=payment_status_choices , default="P")
    total_price = models.FloatField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    customer_name = models.CharField(max_length=500, blank=True, null=True)
    customer_email = models.CharField(max_length=500, blank=True, null=True)
    customer_gender = models.CharField(max_length=1, choices=gender_choices, blank=True, null=True)
    customer_address = models.CharField(max_length=500, blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8 , decimal_places=2 )

    def __str__(self):
        return self.product.title

    def get_total_price(self):
        return self.quantity * self.product.unit_price

    class Meta:
        verbose_name_plural = 'Order Items'

class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username