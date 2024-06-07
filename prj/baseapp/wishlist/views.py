from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from baseapp.utils import get_common_context, get_totals
from baseapp.wishlist.wishlistModel import Wishlist
from baseapp.banner.bannerModel import *

@login_required
def wishlist(request):
    # Get totals
    totals = get_totals(request.user)
    
    # Get wishlist items
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    # Get common context
    common_context = get_common_context()
    
    # Merge contexts
    context = {
        'wishlist_items': wishlist_items,
        'total_cart_items': totals['total_cart_items'],
        'total_wishlist_items': totals['total_wishlist_items']
    }
    context.update(common_context)
    banner = Banner.objects.filter(page='wishlist').first()  # Using filter() instead of get()
    context['banner'] = banner
    
    return render(request, 'products/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        Wishlist.objects.get_or_create(user=request.user, product_id=product_id)
        return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    if request.method == 'POST':
        Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
        return redirect('wishlist')
