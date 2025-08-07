from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..models import Timetables, Subjects, Shifts, Times, SubjectChanges, ProfessorChanges
import datetime
from ..decorators import admin_required, group_required
from .functions import check_if_professor, professors_group_name


@group_required(redirect_page='waiting')
@login_required(login_url='login')
def changes_subject(request):
    args = {
        'shifts': Shifts.objects.all(),
        'professor': check_if_professor(request)
    }
    if request.method == 'POST':
        user_id = request.user.id
        change_date = request.POST.get('change_date')
        shift = request.POST.get('shift')
        time = Times.objects.get(shift_id=shift, class_number=request.POST.get('class_number')).id
        day = datetime.datetime.strptime(change_date, '%Y-%m-%d').weekday() + 1
        subject = Subjects.objects.get(id=Timetables.objects.get(user_id=user_id, shift_id=shift, time_id=time, day_id=day).subject_id)
        changes_object = SubjectChanges.objects.create(professor=request.user, subject=subject, date=change_date, active=False)
        changes_object.save()
    return render(request, 'changes/changes_subject.html', args)


@group_required(redirect_page='waiting')
@login_required(login_url='login')
def changes_professor(request):
    args = {
        'professor': check_if_professor(request)
    }
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        changes_object = ProfessorChanges.objects.create(professor=request.user, start_date=start_date, end_date=end_date, active=False)
        changes_object.save()
    return render(request, 'changes/changes_professor.html', args)


@admin_required(redirect_page='home')
def approve_changes_professor(request):
    if request.method == 'POST':
        professor = request.POST.get('professor')
        change_request = request.POST.get('change').split(' | ')
        change_object = ProfessorChanges.objects.get(start_date=change_request[2].split(' - ')[0], end_date=change_request[2].split(' - ')[1], professor_id=User.objects.get(username=change_request[0]).id)
        change_object.change_id = professor
        change_object.active = True
        change_object.save()

    args = {
        'changes': ProfessorChanges.objects.filter(change_id=None),
        'professors': User.objects.filter(groups__name=professors_group_name)
    }
    return render(request, 'admin/changes/approve_changes_professor.html', args)


@admin_required(redirect_page='home')
def approve_changes_subject(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        change_request = request.POST.get('change').split(' | ')
        print(change_request)
        change_object = SubjectChanges.objects.get(date=change_request[4], subject_id=Subjects.objects.get(long_name=change_request[1], short_name=change_request[2]).id, professor_id=User.objects.get(username=change_request[0]).id)
        change_object.change_id = subject
        change_object.active = True
        change_object.save()

    args = {
        'changes': SubjectChanges.objects.filter(change_id=None),
        'subjects': Subjects.objects.all()
    }
    return render(request, 'admin/changes/approve_changes_subject.html', args)
