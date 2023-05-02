from django.shortcuts import render, redirect
from book.models import Book, Bookinfo
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Transaction, TransactionItem
from datetime import datetime, timedelta

@login_required(login_url="/login")
def cart_add(request, id):
    current_user = request.user
    try:
        cart = Cart.objects.get(user=current_user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            user = current_user
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
    current_user = request.user
    if request.method == 'POST':
        borrow_date = request.POST.get('borrow_date')
        return_date = request.POST.get('return_date')
        new_transaction = Transaction.objects.create(
            user = current_user,
            rental_date = borrow_date,
            return_date = return_date,
        )

        is_cart_exist = Cart.objects.filter(user=current_user).exists()
        if is_cart_exist:
            cart = Cart.objects.get(user_id=request.user)
            list_item_cart = CartItem.objects.filter(cart=cart)
            for item in list_item_cart:
                TransactionItem.objects.create(
                    transaction = new_transaction,
                    book = item.book
                )
                product = CartItem.objects.get(cart=cart, book=item.book)
                product.delete()
            if not CartItem.objects.filter(cart=cart).exists():
                cart.delete()
            return redirect("{% url 'cart:transaction_list' %}")
        new_transaction.delete()
        return redirect("{% url 'cart:cart_detail' %}")
    return redirect("{% url 'cart:transaction_view' %}")

def list_transaction(request):
    current_user = request.user
    list_of_transaction = Transaction.objects.filter(user_id=current_user)
    list_of_items = []
    for transaction in list_of_transaction:
        list_of_item = TransactionItem.objects.filter(transaction = transaction)
        pair = {transaction: list(list_of_item)}
        list_of_items.append(pair)

    return render(request, 'pages/list_transaction.html', {
            'list_of_transaction': list_of_transaction,
            'list_of_items': list_of_items,
            'crr1': current_user.user,
            'crr2': current_user
        })
    
