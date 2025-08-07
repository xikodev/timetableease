from django.contrib import admin
from . models import Timetables, Subjects

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    fields = ('long_name', 'short_name')

@admin.register(Timetables)
class TimetablesAdmin(admin.ModelAdmin):
    fields = ('user', ('subject', 'classname', 'room'), ('shift', 'day'), ('start_time_h', 'start_time_m'), ('end_time_h', 'end_time_m'))
    list_filter = ('subject', 'classname', 'shift', 'day')
