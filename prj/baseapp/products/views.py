from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import F
from .subproductModel import SubProduct, EachProduct
from .comboModel import *
from rest_framework import serializers
from baseapp.banner.bannerModel import *
from baseapp.utils import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = EachProduct
        fields = ['name', 'rating', 'discount']

def product_detail(request, id):
    product = get_object_or_404(EachProduct, id=id)
    mainimg = product.images.filter(is_main_image=True).first()
    context = get_common_context()
    banner = Banner.objects.filter(page='about').first()  # Using filter() instead of get()
    context['banner'] = banner
    x = {'product': product, 'mainimg': mainimg}
    context.update(x)
    return render(request, 'products/product-details.html', context)

def top_rated_products(request):
    sub_products = SubProduct.objects.all()

    top_rated_products_per_subproduct = []
    for sub_product in sub_products:
        top_rated_product = EachProduct.objects.filter(parent_product=sub_product).annotate(
            calculated_rating=F('rating') * (F('discount') / 100)).order_by('-calculated_rating').first()
        if top_rated_product:
            top_rated_products_per_subproduct.append({
                'sub_product': sub_product.name,
                'top_rated_product': {
                    'name': top_rated_product.name,
                    'rating': top_rated_product.calculated_rating,  # Use the new annotation name
                    'discount': top_rated_product.discount
                }
            })

    return JsonResponse(top_rated_products_per_subproduct, safe=False)

def latest_products(request):
    # Retrieve the latest 10 products added to the database, ordered by creation time
    latest_products = EachProduct.objects.order_by('-id')[:10]
    
    context = {
        'latest_products': latest_products
    }
    return render(request, 'products/latest_products.html', context)


def ajax_search_products(request):
    query = request.GET.get('query', '')
    if query:
        products = EachProduct.objects.filter(name__icontains=query)
        results = [{'id': product.id, 'name': product.name} for product in products]
    else:
        results = []
    return JsonResponse(results, safe=False)



def combo_list(request):
    combos = Combo.objects.all()
    context = {'combos': combos}
    return render(request, 'test.html', context)