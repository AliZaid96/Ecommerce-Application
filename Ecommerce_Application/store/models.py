from django.db import models
import datetime
import os

def filepath(request,filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (current_time,old_name)
    return os.path.join("uploads/",filename)

# Models to store categories for product
class Categories(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product', on_delete=models.SET_NULL, null=True ,blank=True, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

# Model to store promotions for the product
class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = 'Promotions'

# Model to store products information
class Product(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    unit_price=models.DecimalField(max_digits=8, decimal_places=2 )
    inventory=models.IntegerField()
    added = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_update=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Categories, on_delete=models.PROTECT)
    promotions=models.ManyToManyField(Promotion, blank=True)
    img = models.ImageField(upload_to=filepath, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Products'