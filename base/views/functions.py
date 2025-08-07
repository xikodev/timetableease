import datetime
from django.contrib.auth.models import User
from ..models import Timetables, Shifts, Times, Days, Subjects, SubjectChanges, ProfessorChanges

professors_group_name = 'Profesori'


def check_if_professor(request):
    if request.user.groups.filter(name=professors_group_name).exists():
        return True
    return False


def get_timetable(request, shift, select_classname=None, select_professor=None):
    shift = Shifts.objects.get(shift=shift.upper())
    if select_classname:
        timetable_object = Timetables.objects.filter(classname_id=select_classname, shift=shift)
    elif select_professor:
        timetable_object = Timetables.objects.filter(user=select_professor, shift=shift)
    else:
        if check_if_professor(request):
            timetable_object = Timetables.objects.filter(user=request.user, shift=shift)
        else:
            timetable_object = Timetables.objects.filter(classname=request.user.groups.all()[0], shift=shift)

    timetable = []
    time_objects = set()
    for time in Times.objects.filter(shift_id=shift.id).order_by('time'):
        timetable.append(['', '', '', '', '', ''])
        time_objects.add(time)

    times = []
    i = 0
    for time in time_objects:
        times.append(time.time)
        timetable[i][0] = time
        i += 1

    class SubjectObject:
        def __init__(self, subject, change):
            self.room = subject.room
            self.user = subject.user
            self.subject = subject.subject
            self.change = change
            self.day = subject.day_id
            self.time = subject.time

    for i in range(len(timetable)):
        for j in range(len(timetable[0])):
            for subject in timetable_object.all():
                subject_changes_object = SubjectChanges.objects.filter(professor_id=subject.user_id, active=True)
                professor_changes_object = ProfessorChanges.objects.filter(professor_id=subject.user_id, active=True)
                try:
                    subject_changes_day = datetime.datetime.strptime(str(subject_changes_object.get(subject_id=subject.subject_id).date), '%Y-%m-%d').weekday() + 1
                except SubjectChanges.DoesNotExist:
                    subject_changes_day = None
                if subject.day_id == subject_changes_day and subject.time == timetable[i][0]:
                    subject_object = SubjectObject(subject, change=True)
                    subject_object.subject = Subjects.objects.get(id=subject_changes_object.get(subject_id=subject.subject_id).change_id)
                    timetable[i][subject_object.day] = subject_object
                else:
                    found = False
                    for professor in professor_changes_object:
                        start_date = professor.start_date
                        end_date = professor.end_date
                        delta = datetime.timedelta(days=1)
                        try:
                            professor_changes_day = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').weekday() + 1
                        except ProfessorChanges.DoesNotExist:
                            professor_changes_day = None
                        while start_date <= end_date:
                            if subject.day_id == professor_changes_day and subject.time == timetable[i][0]:
                                subject_object = SubjectObject(subject, change=True)
                                subject_object.user = User.objects.get(id=professor_changes_object.get(professor_id=subject.user_id).change_id)
                                timetable[i][subject_object.day] = subject_object
                                found = True
                                break
                            start_date += delta

                    if not found and subject.time == timetable[i][0]:
                        subject_object = SubjectObject(subject, change=False)
                        timetable[i][subject_object.day] = subject_object

    args = {
        'times': times,
        'timetable': timetable,
        'shift': shift.shift
    }
    if check_if_professor(request):
        args['professor'] = True

    return args
