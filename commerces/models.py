from django.db import models
from django.conf import settings
# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('delivering', 'Delivering'),
        ('done', 'Done')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('catalogs.Restaurant', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item_name = models.CharField(max_length=255)
    menu_item_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)
    line_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    option_name = models.CharField(max_length=255)
    place_delta = models.DecimalField(max_digits=8, decimal_places=2)

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2)

class OrderPromo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    applied_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    class Meta:
        unique_together = ('order', 'promo_code')