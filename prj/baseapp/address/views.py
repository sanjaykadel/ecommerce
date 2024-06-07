from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render, redirect
from .addressModel import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from baseapp.utils import *


@login_required
def address(request):
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            
            # If no addresses exist for the user, set the new address as default
            if not addresses.exists():
                new_address.is_default = True
            
            new_address.save()
            return redirect('address')
    else:
        form = AddressForm()
    context = get_common_context()
    address = {"addresses": addresses, "form": form}
    context.update(address)
    totals = get_totals(request.user)
    context.update({
            'total_cart_items': totals['total_cart_items'],
            'total_wishlist_items': totals['total_wishlist_items'],
        })
    return render(request, "myaddress.html", context)



def edit_address(request, address_id):
    address = Address.objects.get(pk=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('address')
    else:
        form = AddressForm(instance=address)
    return render(request, "myaddress.html", {"form": form})

def delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = Address.objects.get(pk=address_id)
        address.delete()
        messages.success(request, 'Address deleted successfully.')
    return redirect('address')  # Redirect to address list page