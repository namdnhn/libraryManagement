from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from home.forms import RegistrationForm
from django.contrib.auth import get_user_model

# Hash for password
Account = get_user_model()


def index(request):
    if not request.user.username:
        return render(request, 'pages/home.html')
    elif request.user.is_authenticated:
        username = request.user.username
        # Check if account signed in for the first time -> redirect to change profile page
        return render(request, 'pages/home.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "Username or Password is incorrect!!!")

    return render(request, 'pages/login.html')


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

    return render(request, 'pages/signup.html', {'form': form})


def LogoutPage(request):
    logout(request)
    return redirect('login')
