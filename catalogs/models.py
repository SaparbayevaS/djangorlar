from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255)

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name =  models.CharField(max_length=255)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

class Category(models.Model):
    name = models.CharField(max_length=255)

class ItemCategory(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = models.IntegerField()

class Option(models.Model):
    name = models.CharField(max_length=255)

class ItemOption(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    price_delta = models.DecimalField(max_digits=8, decimal_places=2)
    is_default = models.BooleanField(default=False)