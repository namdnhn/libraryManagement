from django.contrib import messages
from django.shortcuts import render, redirect

from home.models import Account
from staff.models import Staff
from .forms import RegistrationForm
from .models import Store
from datetime import datetime


def staffsListView(request):
    if request.user.is_authenticated and request.user.is_staff and request.user.staff.position:
        cusList = []
        for d in Staff.objects.all():
            if d.position == 0 and d.store == request.user.staff.store:
                cusList.append({
                    'id': d.id,
                    'name': ' '.join([d.fname, d.lname]),
                    'gender': 'Male' if d.gender == 1 else 'Female',
                    'age': datetime.now().year - d.birthday.year,
                    'phone': d.phone,
                    'activated': 'Yes' if d.account.is_active else 'No'
                })

        return render(request, 'pages/staffs.html', {'staffs': cusList})

    return redirect('home:home')


def staff_profile(request, user_id):
    if request.user.is_authenticated and request.user.is_staff and request.user.staff.position:
        user = Staff.objects.get(id=user_id)
        store = Store.objects.get(address=request.user.staff.store)
        stores = Store.objects.all()
        if request.method == 'POST':
            if 'edit_store' in request.POST:
                user.store_id = request.POST['store']
                user.save()
                messages.success(request, 'Change store successfully!')
            elif 'deactivate' in request.POST:
                user.account.is_active = 0
                user.account.save()
                messages.success(request, f'Deactivate {user.account.username} successfully!')
            else:
                acc = user.account
                acc.set_password(acc.username)
                acc.save()
                messages.success(request, 'Change password successfully!')

        return render(request, 'pages/staff_profile.html',
                      {'user': user, 'account': user.account, 'store': store, 'stores': stores})

    return redirect('home:home')


def staffRegister(request):
    if request.user.is_authenticated and request.user.is_staff and request.user.staff.position:
        if request.method == 'POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            birthday = request.POST.get('birthday')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            username = request.POST.get('username')
            email = request.POST.get('email')
            store = request.user.staff.store

            if Account.objects.filter(username=username).exists():
                messages.error(request, 'This username is already used. Please choose another username!')
                return render(request, 'pages/staff_register.html')
            if Account.objects.filter(email=email).exists():
                messages.error(request, 'This email is already used. Please choose another email!')
                return render(request, 'pages/staff_register.html')

            Account.objects.create_user(username=username, email=email, password=username, is_staff=1)
            user = Staff(fname=fname, lname=lname, account=Account.objects.get(username=username), store=store,
                         birthday=birthday, gender=gender, phone=phone, address=address, position=0)
            user.save()
            messages.success(request, "Account is successfully registered")

        return render(request, 'pages/staff_register.html')

    return redirect('home:home')
