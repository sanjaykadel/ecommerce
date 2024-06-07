from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from baseapp.products.subproductModel import EachProduct
from baseapp.utils import get_common_context, get_totals
from baseapp.banner.bannerModel import Banner
from .QuotationModel import Quotation, QuotationItem
import json
from baseapp.models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags






@login_required
def add_to_quotation(request, product_id):
    product = get_object_or_404(EachProduct, pk=product_id)
    user_quotation, created = Quotation.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    # Check if the product is already in the quotation
    quotation_item, item_created = QuotationItem.objects.get_or_create(Quotation=user_quotation, product=product)
    
    # If the item already exists in the quotation, add the new quantity to the existing quantity
    if not item_created:
        quotation_item.quantity += quantity
    else:
        quotation_item.quantity = quantity  # Set quantity if new quotation item

    # Set the price for the quotation item
    quotation_item.price = product.new_price
    quotation_item.save()

    # Prepare data for email
    maildata = {
        'user': request.user,
        'product_name': product.name,
        'product_title': product.intro,
        'price': product.new_price,
        'image': product.image.url,
        'rating': product.rating,
    }

    # Render the email message using an HTML template
    html_message = render_to_string('quotation/mail_product.html', maildata)
    plain_message = strip_tags(html_message)
    subject = 'Product Added to Quotation'
    sender_email = settings.EMAIL_HOST_USER  # Set a default sender email
    recipient_list = [settings.EMAIL_HOST_USER, request.user.email]  # Send to admin and user

    try:
        # Send email
        send_mail(subject, plain_message, sender_email, recipient_list, html_message=html_message)
    except Exception as e:
        print("An error occurred while sending email:", e)

    # Redirect to the getquotation page
    return redirect('Quotation')



@login_required
def get_quotation(request):
    user_Quotation, created = Quotation.objects.get_or_create(user=request.user)
    Quotation_items = user_Quotation.items.all()

    # Calculate the total price for each quotation item
    for item in Quotation_items:
        item.total_price = item.price * item.quantity

    context = get_common_context()  
    banner = Banner.objects.filter(page='about').first()  # Using filter() instead of get()
    context['banner'] = banner

    quotation_totals = {
        'quotation_items': Quotation_items,
        'total_itemss': sum(item.quantity for item in Quotation_items),
        'total_price': sum(item.total_price for item in Quotation_items)
    }
    context.update(quotation_totals)

    totals = get_totals(request.user)
    context.update({
        'total_cart_items': totals['total_cart_items'],
        'total_wishlist_items': totals['total_wishlist_items'],
    })
    x = quotation_totals.get('total_items')
    context['total_items'] = x
    print(context)
    return render(request, 'quotation/getquotation.html', context)

@login_required
@require_POST
@csrf_exempt
def update_quotation_item_quantity(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    new_quantity = data.get('quantity')

    product = get_object_or_404(EachProduct, id=product_id)
    quotation = get_object_or_404(Quotation, user=request.user)
    quotation_item = get_object_or_404(QuotationItem, Quotation=quotation, product=product)
    
    quotation_item.quantity = new_quantity
    quotation_item.total_price = quotation_item.price * new_quantity
    quotation_item.save()
    
    return JsonResponse({
        'quantity': quotation_item.quantity,
        'total_price': quotation_item.total_price
    })

@login_required
def remove_from_quotation(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(EachProduct, id=product_id)
        user_quotation = get_object_or_404(Quotation, user=request.user)
        
        # Check if the item exists in the quotation
        quotation_item = get_object_or_404(QuotationItem, Quotation=user_quotation, product=product)
        quotation_item.delete()

        return redirect('getquotation')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def clear_quotation(request):
    # Get the user's quotation
    user_Quotation = Quotation.objects.get(user=request.user)

    # Delete all quotation items associated with the user's quotation
    user_Quotation.items.all().delete()

    # Redirect back to the quotation page after clearing the quotation
    return redirect('getquotation')


@login_required
def get_mail(request):
    user_quotation = Quotation.objects.get(user=request.user)
    quotation_items = QuotationItem.objects.filter(Quotation=user_quotation)

    subject = f'Quotation Request from {request.user.first_name} {request.user.last_name}'
    total_price = sum(item.quantity * item.product.new_price for item in quotation_items)

    # Prepare the context for the email template
    context = {
        'user': request.user,
        'quotation_items': quotation_items,
        'total_price': total_price
    }

    # Render the email message using an HTML template
    html_message = render_to_string('quotation/quotation_email.html', context)
    plain_message = strip_tags(html_message)
    sender_email = settings.EMAIL_HOST_USER  # Set a default sender email
    recipient_list = [settings.EMAIL_HOST_USER, request.user.email]  # Send to admin and user

    try:
        send_mail(subject, plain_message, sender_email, recipient_list, html_message=html_message)
    except Exception as e:
        print("An error occurred while sending email:", e)

    next_url = request.GET.get('next', 'getquotation')
    return redirect(next_url)
