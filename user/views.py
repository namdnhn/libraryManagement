from django.shortcuts import render, get_object_or_404, redirect
from book.models import Bookinfo
from .models import Comment, Rate
from django.contrib import messages


# Create your views here.
def add_comment(request, book_id):
    book = get_object_or_404(Bookinfo, pk=book_id)
    if request.method == 'POST' and 'comment_text' in request.POST:
        user = request.user
        comment_text = request.POST.get('comment_text')
        if comment_text != '':
            comment = Comment.objects.create(user=user, book=book, comment=comment_text)
            comment.save()
        else:
            messages.error(request, 'Comment không thể trống')
    return redirect('book:detailed_book', id=book_id)


def add_rating(request, book_id):
    book = Bookinfo.objects.get(id=book_id)
    user = request.user

    if request.method == 'POST' and 'rating_value' in request.POST:
        rating_value = int(request.POST.get('rating_value'))
        if rating_value and 1 <= rating_value <= 5:
            if Rate.objects.filter(user=user, book=book).exists():
                rating = Rate.objects.get(book=book, user=user)
                rating.score = rating_value
                rating.save()
                messages.success(request, 'Thay đổi đánh giá sách thành công.')
            else:
                rating = Rate.objects.create(book=book, user=user, score=rating_value)
                rating.save()
                messages.success(request, 'Đánh giá sách thành công.')
        else:
            messages.error(request, 'Đánh giá không hợp lệ.')

    return redirect('book:detailed_book', id=book_id)
