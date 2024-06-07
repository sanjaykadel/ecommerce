from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms in the inline

class EachProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class ComboProductInline(admin.TabularInline):
    model = ComboProduct
    extra = 1

class ComboAdmin(admin.ModelAdmin):
    inlines = [ComboProductInline]

    def save_model(self, request, obj, form, change):
        obj.save()  # Save the Combo instance to get an ID

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.calculate_prices()  # Recalculate prices after saving related objects
        form.instance.save()  # Save again to update calculated fields


admin.site.register(Product)
admin.site.register(SubProduct)
admin.site.register(EachProduct , EachProductAdmin)
admin.site.register(Profile)
admin.site.register(TeamMember)
admin.site.register(ClientQuery)
admin.site.register(Banner)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Quotation)
admin.site.register(QuotationItem)
admin.site.register(Buy)
admin.site.register(BuyItem)
admin.site.register(Combo,ComboAdmin)