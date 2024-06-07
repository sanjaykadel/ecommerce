from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from baseapp.User.views import *
from django.contrib.auth.views import LoginView, LogoutView
from baseapp.products.views import * 
from baseapp.wishlist.views import *
from baseapp.cart.views import *
from baseapp.Quotation.views import *
from baseapp.address.views import *
from baseapp.buy.views import *




urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.base, name='base'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),
    path('address/', address, name='address'),
    path('delete/', delete_address, name='delete_address'),
    path('edit/<int:address_id>/', edit_address, name='edit_address'),

    path('shop/', views.shop, name='shop'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('ajax/search-products/', ajax_search_products, name='ajax_search_products'),
    path('myaccount',views.account,name='myaccount'),
    path('combo_list',combo_list,name='combo_list'),

    path('getquotation/', get_quotation, name='Quotation'),
    path('update_Quotation_item_quantity/', update_quotation_item_quantity, name='update_Quotation_item_quantity'),
    path('add_to_Quotation/<int:product_id>/', add_to_quotation, name='add_to_Quotation'),
    path('remove_from_quotation/<int:product_id>/', remove_from_quotation, name='remove_from_quotation'),
    path('clear-Quotation/', clear_quotation, name='clear_Quotation'),
    path('Quotation_mail/', get_mail, name='get_mail'),
    
    
    
    path('cart/', cart, name='cart'),
    path('update_cart_item_quantity/', update_cart_item_quantity, name='update_cart_item_quantity'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
     path('add_all_to_cart/', add_all_to_cart, name='add_all_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),


    path('wishlist/', wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),


    path('buy/', buy, name='buy'),
    path('update_buy_item_quantity/', update_buy_item_quantity, name='update_buy_item_quantity'),
    path('add_to_buy/<int:product_id>/', add_to_buy, name='add_to_buy'),
     path('add_all_to_buy/', add_all_to_buy, name='add_all_to_buy'),
    path('remove_from_buy/<int:product_id>/', remove_from_buy, name='remove_from_buy'),
    path('clear-buy/', clear_buy, name='clear_buy'),


    path('test/', views.test, name='test'),
    


    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
