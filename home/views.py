from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from home.forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

Account = get_user_model()


def index(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            if not request.user.user.lname:
                messages.warning(request, "Please change your profile first!")
                return redirect('home/profile')
        elif request.user.is_staff and request.user.staff.position:
            return redirect('store:staffs_list')
        elif request.user.is_staff:
            return redirect('staff:customers_list')

    return render(request, 'pages/home.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "Username or Password is incorrect!!!")

    return render(request, 'pages/pages-login.html')


def SignupPage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'pages/pages-register.html', {'form': form})


def LogoutPage(request):
    logout(request)
    return redirect('/login')


def ProfilePage(request):
    if request.user.is_authenticated:
        account = Account.objects.get(id=request.user.id)
        if request.method == 'POST':
            if 'old_password' in request.POST:
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Your password was successfully updated!')
                return render(request, 'pages/users-profile.html', {'user': account.user, 'account': account, 'form': form})
            else:
                user = account.user
                user.fname = request.POST.get('first_name')
                user.lname = request.POST.get('last_name')
                user.birthday = request.POST.get('birthday')
                user.gender = request.POST.get('gender')
                user.phone = request.POST.get('phone')
                user.address = request.POST.get('address')
                if request.FILES:
                    user.avatar = request.FILES['avatar']
                user.save()

        return render(request, 'pages/users-profile.html', {'user': account.user, 'account': account})

    return redirect('/')
