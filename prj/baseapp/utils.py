from baseapp.models import *
from baseapp.wishlist.wishlistModel import Wishlist

from django.db.models import Max

from .models import Product, SubProduct, EachProduct, Profile, Cart, Wishlist

def get_totals(user):
    # Calculate total items in the cart
    user_cart, created = Cart.objects.get_or_create(user=user)
    cart_items = user_cart.items.all()
    total_cart_items = sum(item.quantity for item in cart_items)
    
    # Calculate total items in the wishlist
    total_wishlist_items = Wishlist.objects.filter(user=user).count()
    
    return {
        'total_cart_items': total_cart_items,
        'total_wishlist_items': total_wishlist_items
    }

def get_common_context():
    # Get common data for all views
    products = Product.objects.all()
    sub_products = SubProduct.objects.all()
    each_products = EachProduct.objects.all()
    profile = Profile.objects.first()  # Assuming you have only one profile instance
    logo_url = profile.logo.url if profile and profile.logo else None

    # Get top-rated products for each sub-product
    top_rated_products_per_subproduct = []
    for sub_product in sub_products:
        top_rated_products = EachProduct.objects.filter(parent_product=sub_product).order_by('-rating')[:2]
        if top_rated_products:
            top_rated_products_per_subproduct.append({
                'sub_product': sub_product,
                'top_rated_products': top_rated_products
            })

    # Get featured products
    featured_products = EachProduct.objects.filter(is_featured=True)

    context = {
        'products': products,
        'sub_products': sub_products,
        'each_products': each_products,
        'profile': profile,
        'logo_url': logo_url,
        'top_rated_products_per_subproduct': top_rated_products_per_subproduct,
        'featured_products': featured_products,  # Add featured products to context
    }
    
    return context