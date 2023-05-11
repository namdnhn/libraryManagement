from datetime import datetime
from django.shortcuts import redirect, render
from .models import Bookinfo, Book
from django.db.models import Q
from user.models import Comment, Rate
from django.contrib.auth import get_user_model

Account = get_user_model()

# Create your views here.
def bookpage(request, id):
    book = Bookinfo.objects.get(id=id)
    score_rate = 0
    comments = Comment.objects.filter(book=book)
    rates = Rate.objects.filter(book=book)
    did_rate = Rate.objects.filter(book=book, user=request.user).exists()
    if Rate.objects.filter(book=book).exists():
        sum = 0
        for rate in rates:
            sum += rate.score
        score_rate = float(sum) / rates.count()
        book.rating = score_rate
        book.save()
    if request.user.is_authenticated:
        expiredAccount = False
        if not request.user.user.expired_date or request.user.user.expired_date < datetime.now().date():
            expiredAccount = True
        book_count = Book.objects.filter(info=book, store=request.user.user.current_store, status=0).count()
        return render(request, 'bookshowing.html', {'book': book, 
                                                    'book_count': book_count,
                                                    'expiredAccount': expiredAccount, 
                                                    'comments': comments,
                                                    'comments_count': comments.count(),
                                                    'score_rate': round(score_rate, 1), 
                                                    'rate_count': rates.count(),
                                                    'did_rate': did_rate})
    else:
        return render(request, 'bookshowing.html', {'book': book, 
                                                    'comments': comments,
                                                    'comments_count': comments.count(),
                                                    'score_rate': round(score_rate, 1), 
                                                    'rate_count': rates.count(),
                                                    'did_rate': did_rate})


def book_list(request):
    books = Bookinfo.objects.all()
    if request.user.is_authenticated:
        if request.user.user.current_store:
            store = request.user.user.current_store
            book_and_avai = []
            for book in books:
                is_available = is_available_in_store(book, store)
                book_and_avai.append((book, is_available))
            return render(request, 'booklist.html', {'books': book_and_avai})

        else:
            return redirect('store:change_store')
    else:
        book_and_avai = []
        for book in books:
            book_and_avai.append((book, True))
        return render(request, 'booklist.html', {'books': book_and_avai})
    
def is_available_in_store(book, store):
    return Book.objects.filter(info=book, store=store, status=0)


def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        print(q)
        books = Bookinfo.objects.order_by('-title').filter(Q(title__icontains=q) | Q(description__icontains=q))
        book_count = books.count()
    return render(request, 'booksearch.html', {
        'books': books,
        'q': q,
        'book_count': book_count
    })

def view_book_by_genre(request, genre):
    books = Bookinfo.objects.order_by('-title').filter(Q(genre__icontains=genre))
    book_count = books.count()
    return render(request, 'booksearchbygenre.html', {
        'books': books,
        'genre': genre,
        'book_count': book_count
    })