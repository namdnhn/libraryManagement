from django.contrib import messages
from django.shortcuts import render, redirect
from user.models import User
from datetime import datetime


def customersListView(request):
    if request.user.is_authenticated and request.user.is_active and request.user.is_staff:
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


def user_profile(request, user_id):
    if request.user.is_authenticated and request.user.is_active and request.user.is_staff:
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


