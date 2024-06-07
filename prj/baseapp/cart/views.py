from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from baseapp.cart.cartModel import Cart, CartItem
from baseapp.products.subproductModel import EachProduct
from baseapp.utils import get_common_context, get_totals
from baseapp.banner.bannerModel import Banner
from baseapp.models import *
import json

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(EachProduct, pk=product_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=product)
    
    # If the item already exists in the cart, add the new quantity to the existing quantity
    if not item_created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity  # Set quantity if new cart item

    # Set the price for the cart item
    cart_item.price = product.new_price
    cart_item.save()

    return redirect('cart')

@login_required
def add_all_to_cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    user_quotation = Quotation.objects.get(user=request.user)
    quotation_items = QuotationItem.objects.filter(Quotation=user_quotation)

    for item in quotation_items:
        cart_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
        if item_created:
            cart_item.quantity = item.quantity
            cart_item.price = item.price
        else:
            cart_item.quantity += item.quantity
        cart_item.save()

    # Redirect back to the referring page or a default URL
    next_url = request.GET.get('next', 'cart')
    return redirect(next_url)


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(EachProduct, pk=product_id)
    user_cart = get_object_or_404(Cart, user=request.user)
    
    # Check if the item exists in the cart
    cart_item = get_object_or_404(CartItem, cart=user_cart, product=product)

    # If the item's quantity is greater than 1, decrease its quantity
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # If the item's quantity is 1, remove it from the cart
        cart_item.delete()

    return redirect('cart')

@login_required
def cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.items.all()

    # Calculate the total price for each cart item
    for item in cart_items:
        item.total_price = item.price * item.quantity

    context = get_common_context()  
    banner = Banner.objects.filter(page='about').first()  # Using filter() instead of get()
    context['banner'] = banner

    cart_totals = {
        'cart_items': cart_items,
        'total_items': sum(item.quantity for item in cart_items),
        'total_price': sum(item.total_price for item in cart_items)
    }
    context.update(cart_totals)

    totals = get_totals(request.user)
    context.update({
        'total_cart_items': totals['total_cart_items'],
        'total_wishlist_items': totals['total_wishlist_items'],
    })

    return render(request, 'products/cart.html', context)

@login_required
@require_POST
@csrf_exempt
def update_cart_item_quantity(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    new_quantity = data.get('quantity')

    product = get_object_or_404(EachProduct, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    cart_item.quantity = new_quantity
    cart_item.total_price = cart_item.price * new_quantity
    cart_item.save()
    
    return JsonResponse({
        'quantity': cart_item.quantity,
        'total_price': cart_item.total_price
    })

@login_required
def clear_cart(request):
    # Get the user's cart
    user_cart = Cart.objects.get(user=request.user)

    # Delete all cart items associated with the user's cart
    user_cart.items.all().delete()

    # Redirect back to the cart page after clearing the cart
    return redirect('cart')

