from datetime import datetime
from django.shortcuts import render
from .models import Bookinfo
from django.db.models import Q
from user.models import Comment, Rate


# Create your views here.
def bookpage(request, id):
    book = Bookinfo.objects.get(id=id)
    score_rate = 0
    expiredAccount = False
    if not request.user.user.expired_date or request.user.user.expired_date < datetime.now().date():
        expiredAccount = True
    comments = Comment.objects.filter(book=book)
    rates = Rate.objects.filter(book=book)
    if Rate.objects.filter(book=book).exists():
        sum = 0
        for rate in rates:
            sum += rate.score
        score_rate = float(sum) / rates.count()
    return render(request, 'bookshowing.html', {'book': book, 
                                                'expiredAccount': expiredAccount, 
                                                'comments': comments,
                                                'comments_count': comments.count(),
                                                'score_rate': round(score_rate, 1), 
                                                'rate_count': rates.count()})


def book_list(request):
    books = Bookinfo.objects.all()

    return render(request, 'booklist.html', {
        'books': books
    })


def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        books = Bookinfo.objects.order_by('-title').filter(Q(title__icontains=q) | Q(description__icontains=q))
        book_count = books.count()
    return render(request, 'booksearch.html', {
        'books': books,
        'q': q,
        'book_count': book_count
    })
