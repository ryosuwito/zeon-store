from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from store.st_catalog.models import Product, Category
from store.st_shopping_cart.models import Cart, CartItem, WishList, WishListItem
from store.st_shopping_cart import carts, wishlists
from membership.models import Member
#from membership.views import check_host

import datetime
import random

from .forms import ProductCartForm

def home(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    products = Product.objects.filter(is_archived=False).order_by('-pk')[:4]
    featured_products = Product.objects.filter(is_featured=True).order_by('-pk')[0]
    return render(request, 'keskei/index.html', 
        {'cart':cart_object, 
        'products':products,
        'featured_products':featured_products})
    #push error

def product_detail(request, product_pk, **kwargs):
    """
    referal_code = redirect_referal_code(request, kwargs=kwargs)
    if referal_code['code']:
        referer = Member.objects.get(referal_code = referal_code['code'])
    else:
        referer = ''

    if referal_code['message'] == "redirect_to_default":
        return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                reverse('storefront:product_detail', kwargs={'product_pk':product_pk},
                    current_app=request.resolver_match.namespace))
    elif referal_code['message'] == 'redirect_to_referal':
        return HttpResponseRedirect(request.scheme+"://"+referer.user.username+'.'+settings.DEFAULT_HOST + 
                reverse('storefront:product_detail', kwargs={'product_pk':product_pk},
                    current_app=request.resolver_match.namespace))
    """
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    all_product = Product.objects.filter(is_archived=False).exclude(pk=product_pk)
    is_wishlist = False
    if len(all_product) >= 5:
        other_product = random.sample(list(all_product), 4)
    else:
        other_product = random.sample(list(all_product), len(all_product))

    product = Product.objects.get(pk=product_pk)
    is_in_wishlist = False

    if request.method == 'POST':
        method = ''
        try:
            method = request.POST['method']
        except:
            pass
        
        if method == 'wishlist':  
            is_wishlist = True 
            wishlist_item = WishListItem.objects.get_or_create(wishlist=wishlist_object, product=product)[0]
       
        elif method == 'cart':
            form = ProductCartForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                quantity = data.get('quantity')
                cart_item = False
                try :
                    cart_item = CartItem.objects.get_or_create(cart=cart_object, product=product)[0]
                except:
                    pass

                if not cart_item.quantity :
                    cart_item.quantity = quantity
                else :
                    cart_item.quantity += int(quantity)

                if request.user.is_authenticated:
                    if referer and not referer == request.user.member:
                        cart_item.product_referal = referer
                else: 
                    if referer:
                        cart_item.product_referal = referer
                    
                cart_item.save()
            
            return HttpResponseRedirect(reverse('cart:index', 
                current_app=request.resolver_match.namespace))

    form = ProductCartForm()

    product = Product.objects.get(pk=product_pk)

    discount = 0
    discounted_price = product.price
    
    if request.user.is_authenticated:
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
            discount = request.user.member.get_level()['BENEFIT']
            discounted_price = product.price * (100 - discount) / 100

    products_in_wishlist = [x.product.id for x in wishlist_object.item_in_wishlist.all()]
    for pk in produreferal_cocts_in_wishlist:
        if product_pk == pk:
            is_in_wishlist = True

    if is_wishlist:
        response = HttpResponseRedirect(reverse("storefront:product_detail", kwargs=
            {'product_pk':product_pk})[:-1]+"#formQuantity")
    else:
        response = render(request, 'storefront/product_detail.html', 
            {'product':product, 
            'other_product':other_product, 
            'cart':cart_object, 
            'wishlist':wishlist_object, 
            'form':form, 
            'is_in_wishlist': is_in_wishlist,
            'discount': discount, 
            'discounted_price': int(discounted_price)})

    return response
    
def index(request, **kwargs):
    """
    referal_code = redirect_referal_code(request, kwargs=kwargs)
    if referal_code['code']:
        referer = Member.objects.get(referal_code = referal_code['code'])

    if referal_code['message'] == "redirect_to_default":
        return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                reverse('storefront:product_all', 
                    current_app=request.resolver_match.namespace))
    elif referal_code['message'] == 'redirect_to_referal':
        return HttpResponseRedirect(request.scheme+"://"+referer.user.username+'.'+settings.DEFAULT_HOST + 
                reverse('storefront:product_all', 
                    current_app=request.resolver_match.namespace))
    """

    try:
        product_list = Product.objects.filter(is_archived=False)
    except:
        product_list=''
    if not product_list:
        product_title = 'Tidak Ada Produk'
    else:
        product_title = 'Menampilkan Semua Produk'
    return paginate_results(request, product_list,product_title)
    
def product_by_category(request, category_pk, **kwargs):
    try:
        kategori = Category.objects.get(pk=category_pk)
        product_list = kategori.products_in_category.filter(is_archived=False)
    except:
        product_list=''
    if not product_list:
        product_title = 'Tidak Ada Produk'
    else:
        product_title = 'Menampilkan Semua Produk %s' % (kategori.name.title())
    return paginate_results(request, product_list,product_title)

def paginate_results(request, product_list,product_title):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    max_page = 4
    min_page = 0
    products = ''
    if product_list:
        try:
            paginator = Paginator(product_list,12)
            page = request.GET.get('page', 1)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            max_page = products.number + 4
            min_page = products.number - 4
        except:
            pass

    try:
        categories = Category.objects.filter(is_archived=False)
    except:
        categories = ''

    response = render(request, 'st_storefront/product_all.html', 
        {'cart':cart_object,
         'wishlist':wishlist_object, 
         'products':products,
         'categories':categories,
         'product_title':product_title,
         'max_page':max_page,
         'min_page':min_page})
    return response
"""
def  redirect_referal_code(request, kwargs):
    try:
        referal_code = kwargs['referal_code']
    except:
        referal_code = ''

    if request.get_host() != settings.DEFAULT_HOST:
        if referal_code:
            return {'code':referal_code, 'message':'redirect_to_referal'}
        else:
            referal_code = check_host(request, pass_variable=True)
            if not referal_code:
                return  {'code':'', 'message': 'redirect_to_default'}
            
    else :
        if referal_code:
            try:
                referer_user = Member.objects.get(referal_code = referal_code)
            except:
                referer_user = ''

            if referer_user:
                return {'code':referal_code, 'message':'redirect_to_referal'}
            else:
                return {'code':'', 'message': 'redirect_to_default'}

    return {'code':referal_code, 'message': 'do_nothing'}
"""