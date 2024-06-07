from django.db import models


PAGE_CHOICES = (
    ('index', 'index'),
    ('about', 'about'),
    ('contact', 'contact'),
    ('shop', 'shop'),
    ('wishlist', 'wishlist'),
    ('cart', 'cart'),
    ('myaccount', 'myaccount'),
    # Add more choices as needed
)

class Banner(models.Model):
    page = models.CharField(max_length=100, choices=PAGE_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    banner = models.ImageField(upload_to='banners/')
    banner1 = models.ImageField(upload_to='banners/', blank=True)
    hero = models.ImageField(upload_to='hero/', blank=True)
    section = models.ImageField(upload_to='sections/', blank=True)
    section1 = models.ImageField(upload_to='sections/', blank=True)

    def __str__(self):
        return f"{self.get_page_display()} - {self.title}"
