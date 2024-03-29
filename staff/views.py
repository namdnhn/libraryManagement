from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import config
from book.models import Bookinfo, Book
from cart.models import Transaction, TransactionItem
from store.models import Store
from user.models import User, Comment, Rate
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

        return render(request, 'pages/customers.html', {'customers': cusList, 'account': request.user})
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
                    'available': Book.objects.filter(info=d, store=ch, status=Book.Status.AVAILABLE).count()
                })

        return render(request, 'pages/books.html', {'books': cusList, 'account': request.user})
    return redirect('home:home')


@login_required(login_url="/login")
def editBookProfile(request, id):
    if request.user.is_active and request.user.is_staff:
        book = Bookinfo.objects.get(id=id)
        score_rate = 0
        comments = Comment.objects.filter(book=book)
        rates = Rate.objects.filter(book=book)
        if Rate.objects.filter(book=book).exists():
            score_rate = sum([rate.score for rate in rates]) / rates.count()

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
                book.description = request.POST.get('description')
                if request.FILES:
                    print(request.FILES)
                    book.book_image = request.FILES['image']
                book.save()

        return render(request, 'bookshowing.html', {'book': book, 'account': request.user, 'editmode': editmode, 'genres': config.genres.items(),
                                                    'comments': comments,
                                                    'comments_count': comments.count(),
                                                    'score_rate': round(score_rate, 1),
                                                    'rate_count': rates.count()})

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
            count = int(request.POST.get('count'))
            genre = ''
            if 'genre' in request.POST:
                genre = ', '.join([config.genres[s] for s in dict(request.POST)['genre']])

            if not Bookinfo.objects.filter(title=title, author=author, cover_price=price).count():
                Bookinfo.objects.create(title=title, author=author, cover_price=price, description='', pages=0,
                                        rating=0, genre=genre)
            elif genre != '':
                info = Bookinfo.objects.get(title=title, author=author, cover_price=price)
                info.genre = genre
                info.save()

            info = Bookinfo.objects.get(title=title, author=author, cover_price=price)
            if count > 0:
                for i in range(count):
                    Book.objects.create(info=info, store=request.user.staff.store, status=0)
                messages.success(request, f'Book {title} is added successfully')
            else:
                availBook = Book.objects.filter(info=info, store=request.user.staff.store, status=0)
                if availBook.count() < abs(count):
                    messages.error(request, "Not enough available books in store to export!")
                else:
                    for b in availBook:
                        if count == 0:
                            break
                        b.delete()
                        count += 1
                    messages.success(request, f'Book {title} is exported successfully')

        return render(request, 'pages/add_book.html', {'bookinfo': data, 'account': request.user, 'genres': config.genres.items()})
    return redirect('home:home')


@login_required(login_url="/login")
def transactionProfile(request, id):
    if request.user.is_active and request.user.is_staff:
        trans = Transaction.objects.get(id=id)
        if request.method == 'POST':
            if 'discard' in request.POST:
                for i in TransactionItem.objects.filter(transaction=trans):
                    i.book.status = Book.Status.AVAILABLE
                    i.book.save()
                trans.delete()
                messages.success(request, "Transaction is discarded successfully")
                return redirect('staff:book_handover')

            else:
                book = Book.objects.get(book_id=request.POST.get('book_id'))
                book.status = Book.Status.AVAILABLE
                book.save()
                item = TransactionItem.objects.get(book=book, transaction=trans)
                item.return_date = datetime.now().date()
                item.save()

        getCountdown = (trans.regis_date - datetime.now().date()).days + config.getBookInterval if trans.trans_status == 1 else 0
        items = []
        trans_done = True
        for i in TransactionItem.objects.filter(transaction=trans):
            items.append({
                'id': i.book.book_id,
                'shortid': str(i.book.book_id)[:8],
                'title': i.book.info,
                'bookInfoID': i.book.info.id,
                'countdown': (trans.rental_date - datetime.now().date()).days + config.returnDateInterval if not i.return_date and trans.rental_date else 0,
                'returnedDate': i.return_date,
                'status': i.book.status
            })
            if not i.return_date:
                trans_done = False
        if trans_done:
            trans.trans_status = Transaction.Status.DONE
            trans.save()

        return render(request, 'pages/transaction_profile.html', {'trans': trans, 'items': items, 'getCountdown': getCountdown, 'account': request.user})
    return redirect('home:home')


@login_required(login_url="/login")
def handOverTransactionView(request):
    if request.user.is_active and request.user.is_staff:
        if request.method == 'POST':
            trans_id = request.POST.get('trans_id')
            print(trans_id)
            trans = Transaction.objects.get(id=trans_id)
            trans.trans_status = Transaction.Status.BORROWING
            trans.rental_date = datetime.now().date()
            trans.save()

            for i in TransactionItem.objects.filter(transaction=trans):
                i.book.status = Book.Status.BORROWING
                i.book.save()

        cusList = []
        for d in Transaction.objects.filter(store=request.user.staff.store):
            cusList.append({
                'id': d.id,
                'customer': d.user.user.fname + ' ' + d.user.user.lname,
                'username': d.user,
                'user_id': d.user.id,
                'getCountdown': (d.regis_date - datetime.now().date()).days + config.getBookInterval if d.trans_status == 1 else 0,
                'status': d.trans_status,
                'overdue': 1 if d.trans_status == Transaction.Status.BORROWING and (d.rental_date - datetime.now().date()).days + config.returnDateInterval < 0 else 0
            })

        return render(request, 'pages/handovers.html', {'trans': cusList, 'account': request.user})
    return redirect('home:home')

