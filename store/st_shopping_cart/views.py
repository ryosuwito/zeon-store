from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from .models import Cart, CartItem, WishListItem
import store.st_shopping_cart.carts as carts
import store.st_shopping_cart.wishlists as wishlists
from membership.models import Member
from store.st_shipping_backend.shipping_check import get_courier, get_cost

def index(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    item_list = cart_object.get_items_in_cart()
    paginator = Paginator(item_list,5)
    page = request.GET.get('page', 1)
    max_page = 4
    min_page = 0
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    max_page = products.number + 4
    min_page = products.number - 4
    discount = 0
    discounted_price = 0
    
    if request.method == 'POST':
        method = request.POST.get('method', 'remove')
        item=""
        if method == 'remove':
            try :
                if request.POST['item'] :
                    item_pk = request.POST['item'].split('_')[1]
                    item = CartItem.objects.get(pk=item_pk)
                    item.delete()
            except:
                pass
        elif method == 'update':
            try :
                if request.POST['item'] :
                    item_pk = request.POST['item'].split('_')[1]
                    item = CartItem.objects.get(pk=item_pk)
                    quantity = request.POST.get('quantity', 1)
                    if int(quantity) > 0:
                        item.quantity = quantity
                        item.save()
            except:
                pass

    discounted_price = cart_object.get_total_price()

    if request.user.is_authenticated:
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
            benefit = request.user.member.get_level()['BENEFIT']
            discount = cart_object.get_total_price() * discount / 100
            discounted_price = cart_object.get_total_price() * (100 - discount) / 100
            if discount <= 0:
                discount = int(discount)
                discounted_price = int(discounted_price)

    return render(request, 'shopping_cart/cart_show_all.html', 
        {'wishlist': wishlist_object,
        'cart':cart_object,
        'products':products,
        'discount':discount,
        'discounted_price':discounted_price,
        'max_page':max_page,
        'min_page':min_page})

def wishlist_index(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    item_list = wishlist_object.get_items_in_wishlist()
    paginator = Paginator(item_list,6)
    page = request.GET.get('page', 1)
    max_page = 4
    min_page = 0
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    max_page = products.number + 4
    min_page = products.number - 4

    if request.method == 'POST':
        item=""
        try :
            if request.POST['item'] :
                item_pk = request.POST['item'].split('_')[1]
                item = WishListItem.objects.get(pk=item_pk)
                item.delete()
        except:
            pass

    return render(request, 'shopping_cart/wishlist_show_all.html', 
        {'wishlist': wishlist_object,
        'cart':cart_object,
        'products':products,
        'max_page':max_page,
        'min_page':min_page})