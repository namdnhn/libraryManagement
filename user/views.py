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
        comment = Comment.objects.create(user=user, book=book, comment=comment_text)
        comment.save()
    return redirect('book:detailed_book', id=book_id)

def add_rating(request, book_id):
    book = Bookinfo.objects.get(id=book_id)
    user = request.user

    if request.method == 'POST' and 'rating_value' in request.POST:
        rating_value = int(request.POST.get('rating_value'))
        if rating_value and rating_value >= 1 and rating_value <= 5:
            # Kiểm tra xem user đã đánh giá sách này chưa
            if Rate.objects.filter(user=user, book=book).exists():
                messages.error(request, 'Bạn đã đánh giá cho cuốn sách này rồi, không thể đánh giá lại.')

            # Lưu đánh giá vào cơ sở dữ liệu
            else:
                rating = Rate.objects.create(book=book, user=user, score=rating_value)
                rating.save()
        else:
            messages.error(request, 'Đánh giá không hợp lệ.')

    return redirect('book:detailed_book', id=book_id)