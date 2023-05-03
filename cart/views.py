from django.shortcuts import render, redirect
from book.models import Book, Bookinfo
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem


@login_required(login_url="/login")
def cart_add(request, id):
    current_user = request.user
    try:
        cart = Cart.objects.get(user=current_user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            user=current_user
        )
    cart.save()

    info = Bookinfo.objects.get(id=id)
    book = Book.objects.get(info=info)
    is_book_exist = CartItem.objects.filter(book=book, cart=cart).exists()
    if not is_book_exist:
        new_book = CartItem.objects.create(
            book=book,
            cart=cart,
            is_active=True
        )
    return redirect("/cart/cart-detail/")


@login_required(login_url="/login")
def item_clear(request, id):
    current_user = request.user
    cart = Cart.objects.get(user=current_user)
    book = Book.objects.get(book_id=id)
    product = CartItem.objects.get(cart=cart, book=book)
    product.delete()

    list_item = CartItem.objects.filter(cart=cart)
    number = list_item.count()
    if number == 0:
        cart.delete()
    return redirect("/cart/cart-detail/")


def total(cart):
    list_item = CartItem.objects.filter(cart=cart)
    tt = 0
    for item in list_item:
        tt += item.book.info.cover_price
    return tt


@login_required(login_url="/login")
def cart_detail(request):
    is_cart_exist = Cart.objects.filter(user=request.user).exists()
    if is_cart_exist:
        cart = Cart.objects.get(user_id=request.user)
        list_item = CartItem.objects.filter(cart=cart)
        tt = total(cart)
        number = list_item.count()
        if number == 0:
            cart.delete()
            return render(request, 'pages/cart.html', {
                'exist': is_cart_exist
            })
        return render(request, 'pages/cart.html', {
            'exist': is_cart_exist,
            'list_item': list_item,
            'total': tt
        })
    return render(request, 'pages/cart.html', {
        'exist': is_cart_exist
    })
