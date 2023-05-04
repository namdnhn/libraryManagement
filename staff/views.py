from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import config
from book.models import Bookinfo, Book
from cart.models import Transaction, TransactionItem
from store.models import Store
from user.models import User
from datetime import datetime


@login_required(login_url="/login")
def customersListView(request):
    if request.user.is_active and request.user.is_staff:
        cusList = []
        for d in User.objects.all():
            cusList.append({
                'id': d.id,
                'name': ' '.join([d.fname, d.lname]),
                'gender': 'Male' if d.gender == 1 else 'Female',
                'age': datetime.now().year - d.birthday.year,
                'phone': d.phone,
                'countdown': (d.expired_date - datetime.now().date()).days if d.expired_date else ''
            })

        return render(request, 'pages/customers.html', {'customers': cusList})
    return redirect('home:home')


@login_required(login_url="/login")
def user_profile(request, user_id):
    if request.user.is_active and request.user.is_staff:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            if 'expired_date' in request.POST:
                user.expired_date = request.POST.get('expired_date')
                user.save()
                messages.success(request, 'Update expired date successfully!')
            else:
                acc = user.account
                acc.set_password(acc.username)
                acc.save()
                messages.success(request, 'Change password successfully!')

        return render(request, 'pages/user_profile.html', {'user': user, 'account': user.account})
    return redirect('home:home')


@login_required(login_url="/login")
def booksListView(request):
    if request.user.is_active and request.user.is_staff:
        cusList = []
        for d in Bookinfo.objects.all():
            for ch in Store.objects.all():
                cusList.append({
                    'id': d.id,
                    'title': d.title,
                    'author': d.author,
                    'price': d.cover_price,
                    'store': ch.address,
                    'available': Book.objects.filter(info=d, store=ch).count()
                })

        return render(request, 'pages/books.html', {'books': cusList})
    return redirect('home:home')


@login_required(login_url="/login")
def editBookProfile(request, id):
    if request.user.is_active and request.user.is_staff:
        book = Bookinfo.objects.get(id=id)
        editmode = False
        if request.method == 'POST':
            if 'edit' in request.POST:
                editmode = True
            else:
                editmode = False
                book.title = request.POST.get('title')
                book.publisher = request.POST.get('publisher')
                book.author = request.POST.get('author')
                book.pages = request.POST.get('pages')
                book.cover_price = request.POST.get('cover_price')
                book.rating = request.POST.get('rating')
                book.description = request.POST.get('description')
                if request.FILES:
                    print(request.FILES)
                    book.book_image = request.FILES['image']
                book.save()

        return render(request, 'bookshowing.html', {'book': book, 'account': request.user, 'editmode': editmode})

    return redirect('home:home')


@login_required(login_url="/login")
def addBookView(request):
    if request.user.is_active and request.user.is_staff:
        data = {'titles': set(), 'authors': set(), 'prices': set()}
        for i in Bookinfo.objects.all():
            data['titles'].add(i.title)
            data['authors'].add(i.author)
            data['prices'].add(i.cover_price)

        if request.method == 'POST':
            title = request.POST.get('title')
            author = request.POST.get('author')
            price = request.POST.get('price')
            if not Bookinfo.objects.filter(title=title, author=author, cover_price=price).count():
                Bookinfo.objects.create(title=title, author=author, cover_price=price, description='', pages=0,
                                        rating=0)

            info = Bookinfo.objects.get(title=title, author=author, cover_price=price)
            Book.objects.create(info=info, store=request.user.staff.store, status=0)
            messages.success(request, f'Book {title} is added successfully')

        return render(request, 'pages/add_book.html', {'bookinfo': data})
    return redirect('home:home')


@login_required(login_url="/login")
def transactionProfile(request, id):
    if request.user.is_active and request.user.is_staff:
        trans = Transaction.objects.get(id=id)
        getCountdown = (trans.regis_date - datetime.now().date()).days + config.getBookInterval if trans.trans_status else 0
        items = []
        for i in TransactionItem.objects.filter(transaction=trans):
            items.append({
                'id': str(i.book.book_id)[:8],
                'title': i.book.info,
                'countdown': (trans.rental_date - datetime.now().date()).days + config.returnDateInterval if not i.return_date and trans.rental_date else 0,
                'returnedDate': i.return_date,
                'status': Book.Status(i.book.status).label
            })

        if request.method == 'POST':
            for i in TransactionItem.objects.filter(transaction=trans):
                i.book.status = Book.Status.AVAILABLE
                i.book.save()
            trans.delete()
            messages.success(request, "Transaction is discarded successfully")
            return redirect('staff:book_handover')

        return render(request, 'pages/transaction_profile.html', {'trans': trans, 'items': items, 'getCountdown': getCountdown})
    return redirect('home:home')


@login_required(login_url="/login")
def handOverTransactionView(request):
    if request.user.is_active and request.user.is_staff:
        editMode = False
        cusList = []
        for d in Transaction.objects.filter(store=request.user.staff.store).order_by('-regis_date'):
            cusList.append({
                'id': d.id,
                'customer': d.user.user.fname + ' ' + d.user.user.lname,
                'username': d.user,
                'getCountdown': (d.regis_date - datetime.now().date()).days + config.getBookInterval if d.trans_status else 0,
                'status': d.trans_status
            })

            if request.method == 'POST':
                print('postttt')

        return render(request, 'pages/handovers.html', {'trans': cusList, 'editMode': editMode})
    return redirect('home:home')


@login_required(login_url="/login")
def returnBooksView(request):
    if request.user.is_active and request.user.is_staff:
        cusList = []
        for d in User.objects.all():
            cusList.append({
                'id': d.id,
                'name': ' '.join([d.fname, d.lname]),
                'gender': 'Male' if d.gender == 1 else 'Female',
                'age': datetime.now().year - d.birthday.year,
                'phone': d.phone,
                'countdown': (d.expired_date - datetime.now().date()).days if d.expired_date else ''
            })

        return render(request, 'pages/handovers.html', {'trans': cusList})
    return redirect('home:home')
