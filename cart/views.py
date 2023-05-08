from django.contrib import messages
from django.shortcuts import render, redirect
from book.models import Book, Bookinfo
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Transaction, TransactionItem
from datetime import datetime, timedelta
from django.shortcuts import redirect, reverse


@login_required(login_url="/login")
def cart_add(request, id):
    expiredAccount = False
    if not request.user.user.expired_date or request.user.user.expired_date < datetime.now().date():
        expiredAccount = True
    if expiredAccount:
        messages.error(request, 'Hãy gia hạn thẻ của bạn để có thể sử dụng chức năng này.')
        return redirect('book:detailed_book', id)

    current_user = request.user
    try:
        cart = Cart.objects.get(user=current_user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            user=current_user
        )
    cart.save()

    book = Bookinfo.objects.get(id=id)
    if not CartItem.objects.filter(book=book, cart=cart).exists():
        new_book = CartItem.objects.create(
            book=book,
            cart=cart,
            is_active=True
        )
        new_book.save()
    return redirect('cart:cart_detail')


@login_required(login_url="/login")
def item_clear(request, id):
    current_user = request.user
    cart = Cart.objects.get(user=current_user)
    book = Bookinfo.objects.get(id=id)
    product = CartItem.objects.get(cart=cart, book=book)
    product.delete()

    list_item = CartItem.objects.filter(cart=cart)
    number = list_item.count()
    if number == 0:
        cart.delete()
    return redirect('cart:cart_detail')


def total(cart):
    list_item = CartItem.objects.filter(cart=cart)
    tt = 0
    for item in list_item:
        tt += item.book.cover_price
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


def view_transaction(request):
    current_user = request.user
    is_cart_exist = Cart.objects.filter(user=request.user).exists()
    if is_cart_exist:
        cart = Cart.objects.get(user=current_user)
        list_item = CartItem.objects.filter(cart=cart)
        number = list_item.count()

        today = datetime.today()
        return_date = today + timedelta(days=7)

        return render(request, 'pages/transaction.html', {
            'exist': is_cart_exist,
            'list_item': list_item,
            'number': number,
            'crr1': current_user.user,
            'crr2': current_user
        })
    else:
        return render(request, 'pages/transaction.html', {
            'exist': is_cart_exist
        })


def create_transaction(request):
    expiredAccount = False
    if not request.user.user.expired_date or request.user.user.expired_date < datetime.now().date():
        expiredAccount = True
    if expiredAccount:
        messages.error(request, 'Hãy gia hạn thẻ của bạn để có thể sử dụng chức năng này.')
        return redirect('cart:transaction_view')

    current_user = request.user
    if request.method == 'POST':
        store = request.POST.get('store')
        borrow_date = request.POST.get('borrow_date')
        return_date = request.POST.get('return_date')
        new_transaction = Transaction.objects.create(
            user=current_user,
            rental_date=borrow_date,
            return_date=return_date,
        )

        is_cart_exist = Cart.objects.filter(user=current_user).exists()
        if is_cart_exist:
            cart = Cart.objects.get(user_id=request.user)
            list_item_cart = CartItem.objects.filter(cart=cart)
            for item in list_item_cart:
                TransactionItem.objects.create(
                    transaction=new_transaction,
                    book=item.book
                )
                product = CartItem.objects.get(cart=cart, book=item.book)
                product.delete()
            if not CartItem.objects.filter(cart=cart).exists():
                cart.delete()
            return redirect('cart:transaction_list')
        new_transaction.delete()
        return redirect('cart:cart_detail')
    return redirect('cart:transaction_view')


def list_transaction(request):
    current_user = request.user
    list_of_transaction = Transaction.objects.filter(user_id=current_user)
    list_of_items = []
    for transaction in list_of_transaction:
        list_of_item = TransactionItem.objects.filter(transaction=transaction)
        pair = {transaction: list(list_of_item)}
        list_of_items.append(pair)

    return render(request, 'pages/list_transaction.html', {
        'list_of_transaction': list_of_transaction,
        'list_of_items': list_of_items,
        'crr1': current_user.user,
        'crr2': current_user
    })
