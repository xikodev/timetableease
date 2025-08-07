from django.shortcuts import render
from django.core.exceptions import *
from django.contrib.auth.models import User, Group
from ..decorators import admin_required
from .functions import get_timetable, professors_group_name
from ..models import Timetables, Subjects, Rooms, Shifts, Days, Hours, Minutes, Times

view_select_professor_global = 0
view_select_classname_global = 0

edit_select_classname_global = 0


@admin_required(redirect_page='home')
def view_timetable_professor(request):
    global view_select_professor_global

    args = {
        'professors': User.objects.filter(groups__name=professors_group_name),
        'selected_professor': view_select_professor_global
    }

    if request.method == 'POST':
        view_select_professor_global = int(request.POST.get('select_professor'))

    return render(request, 'admin/timetable/view_timetable_professor.html', args)


@admin_required(redirect_page='home')
def view_timetable_class(request):
    global view_select_classname_global

    args = {
        'classes': Group.objects.exclude(name=professors_group_name),
        'selected_class': view_select_classname_global
    }

    if request.method == 'POST':
        view_select_classname_global = int(request.POST.get('select_class'))

    return render(request, 'admin/timetable/view_timetable_class.html', args)


@admin_required(redirect_page='home')
def view_timetable_professor_select(request, shift):
    args = get_timetable(request, shift, select_professor=view_select_professor_global)
    args.update({'selected_professor': view_select_professor_global, 'professors': User.objects.filter(groups__name=professors_group_name)})

    return render(request, 'admin/timetable/view_timetable_professor_select.html', args)


@admin_required(redirect_page='home')
def view_timetable_class_select(request, shift):
    args = get_timetable(request, shift, select_classname=view_select_classname_global)
    args.update({'selected_class': view_select_classname_global, 'classes': Group.objects.exclude(name=professors_group_name)})

    return render(request, 'admin/timetable/view_timetable_class_select.html', args)


@admin_required(redirect_page='home')
def create_time(request):
    def check_lenght(temp):
        if len(temp[0]) == 1:
            temp[0] = f'0{temp[0]}'
        if len(temp[1]) == 1:
            temp[1] = f'0{temp[1]}'
        time = f'{temp[0]}:{temp[1]}'

        return time

    def check_duration(temp):
        if int(temp[1]) >= 60:
            temp[0] = str(int(temp[0]) + 1)
            temp[1] = str(int(temp[1]) - 60)

        return temp

    def check_pause(time, temp, start_time_pause, big_pause_duration, small_pause_duration):
        if time == start_time_pause:
            temp[1] = str(int(temp[1]) + big_pause_duration)
        else:
            temp[1] = str(int(temp[1]) + small_pause_duration)

        time = f'{temp[0]}:{temp[1]}'
        return time

    if request.method == 'POST':
        class_number = int(request.POST.get('class_number'))
        shift = request.POST.get('shift')

        start_time_h_class = Hours.objects.get(hour=request.POST.get('start_time_h_class'))
        start_time_m_class = Minutes.objects.get(minute=request.POST.get('start_time_m_class'))
        start_time_class = f'{start_time_h_class}:{start_time_m_class}'

        start_time_h_pause = Hours.objects.get(hour=request.POST.get('start_time_h_pause'))
        start_time_m_pause = Minutes.objects.get(minute=request.POST.get('start_time_m_pause'))
        start_time_pause = f'{start_time_h_pause}:{start_time_m_pause}'

        class_duration = int(request.POST.get('class_duration'))
        big_pause_duration = int(request.POST.get('big_pause_duration'))
        small_pause_duration = int(request.POST.get('small_pause_duration'))

        time = start_time_class

        for n in range(class_number):
            temp = time.split(':')
            temp = check_duration(temp)
            time = check_lenght(temp)

            temp_str = f'{time} - '

            temp[1] = str(int(temp[1]) + class_duration)

            temp = check_duration(temp)
            time = check_lenght(temp)

            temp_str += time

            time = check_pause(time, temp, start_time_pause, big_pause_duration, small_pause_duration)

            time_object = Times.objects.create(class_number=n, shift_id=shift, time=temp_str)
            time_object.save()

    args = {
        'shifts': Shifts.objects.all(),
        'hours': Hours.objects.all(),
        'minutes': Minutes.objects.all()
    }
    return render(request, 'admin/timetable/create_time.html', args)


@admin_required(redirect_page='home')
def create_timetable(request):
    if request.method == 'POST':
        classname = request.POST.get('class')
        shift = request.POST.get('shift')

        for time in Times.objects.all():
            for day in Days.objects.all():
                professor = request.POST.get(f'{time} | {day} | professor')
                subject = request.POST.get(f'{time} | {day} | subject')
                room = request.POST.get(f'{time} | {day} | room')
                try:
                    timetable_object = Timetables.objects.create(user_id=professor, subject_id=subject, classname_id=classname, room_id=room, shift_id=shift, day_id=day.id, time_id=time.id)
                    timetable_object.save()
                except ValueError:
                    pass

    args = {
        'professors': User.objects.filter(groups__name=professors_group_name),
        'subjects': Subjects.objects.all(),
        'shifts': Shifts.objects.all(),
        'classes': Group.objects.exclude(name=professors_group_name),
        'rooms': Rooms.objects.all(),
        'days': Days.objects.all(),
        'times': Times.objects.all()
    }
    return render(request, 'admin/timetable/create_timetable.html', args)


@admin_required(redirect_page='home')
def edit_timetable(request):
    global edit_select_classname_global

    if request.method == 'POST':
        edit_select_classname_global = int(request.POST.get('class'))

    args = {
        'shifts': Shifts.objects.all(),
        'classes': Group.objects.exclude(name=professors_group_name),
        'selected_class': edit_select_classname_global
    }
    return render(request, 'admin/timetable/edit_timetable.html', args)


@admin_required(redirect_page='home')
def edit_timetable_select(request, shift):
    global edit_select_classname_global
    shift = shift.upper()
    if request.method == 'POST':
        for time in Times.objects.all():
            for day in Days.objects.all():
                professor = request.POST.get(f'{time} | {day.id} | professor')
                subject = request.POST.get(f'{time} | {day.id} | subject')
                room = request.POST.get(f'{time} | {day.id} | room')
                print(f'{professor}, {subject}, {room}')
                try:
                    timetable_object = Timetables.objects.get(classname_id=edit_select_classname_global, shift_id=Shifts.objects.get(shift=shift).id, time_id=time.id, day_id=day.id)
                    if professor is not None:
                        timetable_object.user_id = professor
                    if subject is not None:
                        timetable_object.subject_id = subject
                    if room is not None:
                        timetable_object.room_id = room
                    timetable_object.save()
                except Timetables.DoesNotExist:
                    if professor is not None and subject is not None and room is not None:
                        print(f'{edit_select_classname_global} | {shift} | {time.id} | {day.id} | {professor} | {subject} | {room}')
                        timetable_object = Timetables.objects.create(classname_id=edit_select_classname_global, shift_id=Shifts.objects.get(shift=shift).id, time_id=time.id, day_id=day.id, user_id=professor, subject_id=subject, room_id=room)
                        timetable_object.save()

    args = get_timetable(request, shift, select_classname=edit_select_classname_global)
    args.update({
        'professors': User.objects.filter(groups__name=professors_group_name),
        'subjects': Subjects.objects.all(),
        'classes': Group.objects.exclude(name=professors_group_name),
        'rooms': Rooms.objects.all(),
        'days': Days.objects.all(),
        'selected_class': edit_select_classname_global
    })
    return render(request, 'admin/timetable/edit_timetable_select.html', args)


@admin_required(redirect_page='home')
def delete_timetable(request):
    if request.method == 'POST':
        classname = request.POST.get('class')
        timetable_object = Timetables.objects.filter(classname_id=classname)
        timetable_object.delete()

    args = {
        'classes': Group.objects.exclude(name=professors_group_name)
    }
    return render(request, 'admin/timetable/delete_timetable.html', args)
