from django.db import models

class SubProduct(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_icon/', null=True, blank=True)
    description = models.TextField()
    parent_product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EachProduct(models.Model):
    name = models.CharField(max_length=100)
    parent_product = models.ForeignKey('SubProduct', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True) 
    is_featured = models.BooleanField(default=False)
    intro = models.CharField(max_length=500, default='good')
    description = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    custom_content = models.TextField(null=True, blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically calculate the discount if both old_price and new_price are provided
        if self.old_price is not None and self.new_price is not None:
            self.discount = ((self.old_price - self.new_price) / self.old_price) * 100
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(EachProduct, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    is_main_image = models.BooleanField(default=False)  # Designate whether the image is the main image or a detail image

    def __str__(self):
        return f"Image for {self.product.name}"


from django import forms

class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Search for products', max_length=100)
