from django.db import models
from django.contrib.auth.models import User, Group


class Subjects(models.Model):
    long_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return f'{self.long_name} | {self.short_name}'


class Rooms(models.Model):
    room = models.CharField(max_length=5)

    def __str__(self):
        return self.room


class Days(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Shifts(models.Model):
    shift = models.CharField(max_length=1)

    def __str__(self):
        return self.shift


class Times(models.Model):
    class_number = models.IntegerField()
    shift = models.ForeignKey(Shifts, on_delete=models.CASCADE)
    time = models.CharField(max_length=13)

    def __str__(self):
        return f'{self.class_number} | {self.shift} | {self.time}'


class Hours(models.Model):
    hour = models.CharField(max_length=2)

    def __str__(self):
        return self.hour


class Minutes(models.Model):
    minute = models.CharField(max_length=2)

    def __str__(self):
        return self.minute


class Timetables(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    classname = models.ForeignKey(Group, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shifts, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
    time = models.ForeignKey(Times, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Timetables'

    def __str__(self):
        return f'{self.classname} | {self.room} | {self.subject} | {self.shift} | {self.day} | {self.time} | {self.user}'


class ProfessorChanges(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professor_pc')
    change = models.ForeignKey(User, on_delete=models.CASCADE, related_name='change', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField()

    def __str__(self):
        return f'{self.professor} | {self.change} | {self.start_date} - {self.end_date} | {self.active}'


class SubjectChanges(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professor_sc')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='subject')
    change = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='change', null=True, blank=True)
    date = models.DateField()
    active = models.BooleanField()

    def __str__(self):
        return f'{self.professor} | {self.subject} | {self.change} | {self.date} | {self.active}'
