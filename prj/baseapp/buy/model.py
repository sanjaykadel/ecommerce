from django.db import models
from django.contrib.auth.models import User
from baseapp.products.subproductModel import EachProduct

class Buy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class BuyItem(models.Model):
    buy = models.ForeignKey(Buy, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(EachProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in buy"
