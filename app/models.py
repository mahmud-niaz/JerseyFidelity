from django.db import models
from django.db.models import AutoField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


class Customer (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

SIZE_CHOICES = (
    ('S', 'small'),
    ('M', 'medium'),
    ('L', 'large'),
    ('XL', 'extra large'),
)

CATEGORY_CHOICES = (
    ('F', 'FOOTBALL'),
    ('C', 'CRICKET'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField(default='null')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    p_image = models.ImageField(upload_to='product_img')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)
SIZE_CHOICES = (
    ('X', 'small'),
    ('M', 'medium'),
    ('L', 'large'),
    ('XL', 'extra large'),
)


class OrderPlaced (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(choices=SIZE_CHOICES, max_length=2, default='M')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

