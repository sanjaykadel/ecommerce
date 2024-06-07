from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from baseapp.clientquery.forms import ClientQueryForm
from django.contrib import messages 
from baseapp.banner.bannerModel import *
from baseapp.products.views import *
from .utils import *
from baseapp.address.addressModel import *
from baseapp.Quotation.views import *


def base(request):
    return render(request, 'base/base.html')

def about_us(request):
    context = get_common_context()
    if request.user.is_authenticated:
        total = get_totals(request.user)
        context.update(total)
    banner = Banner.objects.filter(page='about').first()
    context['banner'] = banner
    team = TeamMember.objects.all()
    context['team'] = team  

    return render(request, 'mainpage/about.html', context)

def contact(request):
    context = get_common_context()
    if request.user.is_authenticated:
        total = get_totals(request.user)
        context.update(total)
    banner = Banner.objects.filter(page='contact').first()
    context['banner'] = banner

    if request.method == 'POST':
        form = ClientQueryForm(request.POST)
        if form.is_valid():
            client_query = form.save(commit=False)
            client_query.save()

            # Send email to admin
            subject = f'this is query from {form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}'
            message = form.cleaned_data['message']
            sender_email = form.cleaned_data['email']
            recipient_list = [settings.EMAIL_HOST_USER]
            try:
                send_mail(subject, message, sender_email, recipient_list)
                return redirect('contact')
            except Exception as e:
                print("An error occurred while sending email:", e)
        else:
            print(form.errors)
    else:
        form = ClientQueryForm()

    context['form'] = form
    return render(request, 'mainpage/contact.html', context)

def home(request):
    context = get_common_context()
    if request.user.is_authenticated:
        total = get_totals(request.user)
        context.update(total)
        # top product from product views
        toprate = top_rated_products(request)
        context['toprate'] = toprate
    
    banners = Banner.objects.filter(page='index')
    context['banners'] = banners

    # Get banners with non-empty image fields
    for field in ['banner', 'banner1', 'hero', 'section', 'section1']:
        try:
            banner_with_image = banners.filter(**{f'{field}__isnull': False}).first()
            context[f'{field}'] = banner_with_image
        except Banner.DoesNotExist:
            pass
    print(context)
    return render(request, 'mainpage/index.html', context)

def account(request):
    context = get_common_context()
    if request.user.is_authenticated:
        total = get_totals(request.user)
        context.update(total)
        banners = Banner.objects.filter(page='myaccount')
        context['banners'] = banners
        context.update({
            'total_cart_items': total['total_cart_items'],
            'total_wishlist_items': total['total_wishlist_items'],
        })
    return render(request, 'mainpage/myaccount.html', context)

def shop(request):
    context = get_common_context()
    if request.user.is_authenticated:
        total = get_totals(request.user)
        context.update(total)
    banner = Banner.objects.filter(page='shop').first()
    context['banner'] = banner
    if request.user.is_authenticated:
        context.update({
            'total_cart_items': total['total_cart_items'],
            'total_wishlist_items': total['total_wishlist_items'],
        })

    return render(request, 'products/shop.html', context)

def test(request):
    context = get_common_context()
    
    if request.method == 'POST':
        form = ClientQueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('test')  
    else:
        form = ClientQueryForm()

    context['form'] = form

    return render(request, 'test.html', context)
