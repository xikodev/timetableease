from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..decorators import group_required
from .functions import check_if_professor, get_timetable


def redirect_to_home(request):
    return redirect('home')


@group_required(redirect_page='waiting')
@login_required(login_url='login')
def home(request):
    args = {
        'professor': check_if_professor(request)
    }

    return render(request, 'home.html', args)


@group_required(redirect_page='waiting')
@login_required(login_url='login')
def timetable(request, shift):
    args = get_timetable(request, shift)
    return render(request, 'timetable.html', args)
