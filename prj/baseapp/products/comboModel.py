from django.db import models
from baseapp.products.subproductModel import EachProduct

class Combo(models.Model):
    title = models.CharField(max_length=100, default='write title here')
    products = models.ManyToManyField(EachProduct, through='ComboProduct')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Discount as a percentage
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_after_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

    def calculate_prices(self):
        total = sum(product.new_price for product in self.products.all())
        discount_amount = (self.discount / 100) * total
        discounted_total = total - discount_amount

        self.price_before_discount = total
        self.price_after_discount = discounted_total

    def save(self, *args, **kwargs):
        if self.pk:  # Ensure instance has a primary key
            self.calculate_prices()
        super().save(*args, **kwargs)

class ComboProduct(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    product = models.ForeignKey(EachProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
