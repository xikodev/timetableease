import json
from django.contrib.auth.models import User, Group
from django.core.exceptions import *
from django.shortcuts import redirect, render
from .functions import professors_group_name
from ..decorators import admin_required
from ..models import Timetables

edit_user_global = 0


@admin_required(redirect_page='home')
def user_management(request):
    args = {
        'users': User.objects.all()
    }

    if request.method == 'POST':
        user = request.POST.get('user')
        if request.POST.get('edit_user'):
            global edit_user_global
            edit_user_global = user
            return redirect('user_management_edit')
        elif request.POST.get('delete_user'):
            user_object = User.objects.get(id=user)
            user_object.delete()

    return render(request, 'admin/users/user_management.html', args)


@admin_required(redirect_page='home')
def user_management_edit(request):
    user_object = User.objects.get(id=edit_user_global)
    args = {
        'user': user_object
    }

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        if first_name != '':
            user_object.first_name = first_name
        if last_name != '':
            user_object.last_name = last_name
        if email != '':
            user_object.email = email
        user_object.save()

    return render(request, 'admin/users/user_management_edit.html', args)


@admin_required(redirect_page='home')
def create_class(request):
    if request.method == 'POST':
        name = request.POST.get('class')
        class_object = Group.objects.create(name=name)
        class_object.save()

    return render(request, 'admin/users/create_class.html')


@admin_required(redirect_page='home')
def add_users_to_group(request):
    users = User.objects.filter(groups__isnull=True, is_superuser=False)

    try:
        if request.method == 'POST':
            classname = request.POST.get('class')
            for user in users:
                user_id = request.POST.get(user.username)
                user_object = User.objects.get(id=user_id)
                user_object.groups.add(classname)
            return redirect('add_users_to_group')
    except ObjectDoesNotExist:
        pass

    args = {
        'users': users,
        'classes': Group.objects.all()
    }
    return render(request, 'admin/users/add_users_to_group.html', args)


@admin_required(redirect_page='home')
def professor_stats(request):
    def get_info_dict(professor):
        info_dict = {}
        timetables_object = Timetables.objects.filter(user_id=professor)
        info_dict['subjects_lectured'] = len(timetables_object)
        return info_dict

    render(request, 'admin/users/temp.json')

    if request.method == 'POST':
        professor = request.POST.get('professor')
        info_dict = get_info_dict(professor)
        info_json = json.dumps(info_dict, indent=4)
        with open('temp.json', 'w') as f:
            f.write(info_json)

    args = {
        'professors': User.objects.filter(groups__name=professors_group_name)
    }
    return render(request, 'admin/users/professor_stats.html', args)


@admin_required(redirect_page='home')
def upload_stats(request):
    return render(request, 'admin/users/temp.json')
