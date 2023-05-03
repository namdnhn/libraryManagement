from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from book.models import Bookinfo, Book
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
def bookProfile(request):
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

