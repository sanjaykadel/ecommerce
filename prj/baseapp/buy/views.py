from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from baseapp.products.subproductModel import EachProduct
from baseapp.utils import get_common_context, get_totals
from baseapp.banner.bannerModel import Banner
from baseapp.models import *
import json

@login_required
def add_to_buy(request, product_id):
    product = get_object_or_404(EachProduct, pk=product_id)
    user_buy, created = Buy.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    # Check if the product is already in the cart
    buy_item, item_created = BuyItem.objects.get_or_create(user_buy=user_buy, product=product)
    
    # If the item already exists in the cart, add the new quantity to the existing quantity
    if not item_created:
        buy_item.quantity += quantity
    else:
        buy_item.quantity = quantity  # Set quantity if new cart item

    # Set the price for the cart item
    buy_item.price = product.new_price
    buy_item.save()

    return redirect('cart')

@login_required
def add_all_to_buy(request):
    user_buy, created = Buy.objects.get_or_create(user=request.user)
    user_quotation = Quotation.objects.get(user=request.user)
    quotation_items = QuotationItem.objects.filter(Quotation=user_quotation)

    for item in quotation_items:
        buy_item, item_created = BuyItem.objects.get_or_create(user_buy=user_buy, product=item.product)
        if item_created:
            buy_item.quantity = item.quantity
            buy_item.price = item.price
        else:
            buy_item.quantity += item.quantity
        buy_item.save()

    # Redirect back to the referring page or a default URL
    next_url = request.GET.get('next', 'buy')
    return redirect(next_url)


@login_required
def remove_from_buy(request, product_id):
    product = get_object_or_404(EachProduct, pk=product_id)
    user_buy = get_object_or_404(Buy, user=request.user)
    
    # Check if the item exists in the cart
    buy_item = get_object_or_404(BuyItem, user_buy=user_buy, product=product)

    # If the item's quantity is greater than 1, decrease its quantity
    if buy_item.quantity > 1:
        buy_item.quantity -= 1
        buy_item.save()
    else:
        # If the item's quantity is 1, remove it from the cart
        buy_item.delete()

    return redirect('cart')

@login_required
def buy(request):
    user_buy, created = Buy.objects.get_or_create(user=request.user)
    buy_items = user_buy.items.all()

    # Calculate the total price for each cart item
    for item in buy_items:
        item.total_price = item.price * item.quantity

    context = get_common_context()  
    banner = Banner.objects.filter(page='buy').first()  # Using filter() instead of get()
    context['banner'] = banner

    buy_totals = {
        'buy_items': buy_items,
        'total_items': sum(item.quantity for item in buy_items),
        'total_price': sum(item.total_price for item in buy_items)
    }
    context.update(buy_totals)

    totals = get_totals(request.user)
    context.update({
        'total_cart_items': totals['total_cart_items'],
        'total_wishlist_items': totals['total_wishlist_items'],
    })

    return render(request, 'products/buy.html', context)

@login_required
@require_POST
@csrf_exempt
def update_buy_item_quantity(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    new_quantity = data.get('quantity')

    product = get_object_or_404(EachProduct, id=product_id)
    buy = get_object_or_404(Buy, user=request.user)
    buy_item = get_object_or_404(BuyItem, buy=buy, product=product)
    
    buy_item.quantity = new_quantity
    buy_item.total_price = buy_item.price * new_quantity
    buy_item.save()
    
    return JsonResponse({
        'quantity': buy_item.quantity,
        'total_price': buy_item.total_price
    })

@login_required
def clear_buy(request):
    # Get the user's cart
    user_buy = Buy.objects.get(user=request.user)

    # Delete all cart items associated with the user's cart
    user_buy.items.all().delete()

    # Redirect back to the cart page after clearing the cart
    return redirect('buy')

