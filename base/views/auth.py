from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'E-mail ili password polje nije točno')

    return render(request, 'auth/login.html')


def logout_page(request):
    logout(request)
    return redirect('login')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password1')
        if password == password_confirm:
            user_object = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email, password=password)
            user_object.save()
            return redirect('login')
    return render(request, 'auth/register.html')


@login_required(login_url='login')
def waiting_page(request):
    if request.user.groups.all():
        return redirect('timetable')
    return render(request, 'auth/waiting.html')
