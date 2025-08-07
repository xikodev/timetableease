from django.shortcuts import redirect, render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..decorators import group_required
from .functions import check_if_professor


@group_required(redirect_page='waiting')
@login_required(login_url='login')
def settings(request):
    args = {
        'professor': check_if_professor(request)
    }
    return render(request, 'settings/settings.html', args)


@group_required(redirect_page='waiting')
@login_required(login_url='login')
def change_email(request):
    if request.method == 'POST':
        old_email = request.POST.get('old_email')
        new_email = request.POST.get('new_email')
        password_confirmation = request.POST.get('password')
        user_object = User.objects.get(username=old_email)
        if user_object.check_password(password_confirmation):
            try:
                validate_email(new_email)
            except ValidationError:
                print('bad email')
            else:
                user_object.username = new_email
                user_object.email = new_email
                user_object.save()
                return redirect('logout')

    return render(request, 'settings/change_email.html')


@group_required(redirect_page='waiting')
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        password_confirmation = request.POST.get('password_confirm')
        user_object = User.objects.get(username=request.user)
        if user_object.check_password(old_password) and new_password == password_confirmation:
            user_object.set_password(new_password)
            user_object.save()
            return redirect('logout')
    return render(request, 'settings/change_password.html')
