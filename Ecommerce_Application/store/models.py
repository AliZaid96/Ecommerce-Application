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
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2 )
    stripe_price_id = models.CharField(max_length=150)
    inventory = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, blank=True, null=True)
    promotion = models.ManyToManyField(Promotion, blank=True)
    img = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Products'

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    session_ID = models.CharField(max_length=50, default=uuid.uuid4)
    subTotal = models.PositiveIntegerField(default=0)
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
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    def get_number_of_items(self):
        return OrderItem.objects.filter(order=self).count()

    def get_items(self):
        return OrderItem.objects.filter(order=self)

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

# Model to store products information
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    message = models.TextField()
    added = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Contact Us'