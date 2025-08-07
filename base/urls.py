from django.urls import path
from .views import auth, changes, feedback, home, settings, timetable, users

urlpatterns = [
    path('', home.redirect_to_home, name='home'),
    path('home/', home.home, name='home'),
    path('home/<shift>/', home.timetable, name='timetable'),

    path('settings/', settings.settings, name='settings'),
    path('settings/change/email/', settings.change_email, name='change_email'),
    path('settings/change/password/', settings.change_password, name='change_password'),

    path('feedback/', feedback.feedback, name='feedback'),
    path('feedback/thanks', feedback.feedback_thanks, name='feedback_thanks'),

    path('auth/register/', auth.register_page, name='register'),
    path('auth/login/', auth.login_page, name='login'),
    path('auth/logout/', auth.logout_page, name='logout'),
    path('auth/waiting', auth.waiting_page, name='waiting'),

    path('add_users_to_group/', users.add_users_to_group, name='add_users_to_group'),
    path('user_management/', users.user_management, name='user_management'),
    path('user_management/edit/', users.user_management_edit, name='user_management_edit'),
    path('stats/', users.professor_stats, name='stats'),
    path('stats/temp.json', users.upload_stats, name='temp.json'),
    path('create/class/', users.create_class, name='create_class'),

    path('create/timetable/', timetable.create_timetable, name='create_timetable'),
    path('edit/timetable/', timetable.edit_timetable, name='edit_timetable'),
    path('edit/timetable/<shift>/', timetable.edit_timetable_select, name='edit_timetable_select'),
    path('delete/timetable/', timetable.delete_timetable, name='delete_timetable'),
    path('create/time/', timetable.create_time, name='create_time'),
    path('view/timetable/class/', timetable.view_timetable_class, name='view_timetable_class'),
    path('view/timetable/class/<shift>/', timetable.view_timetable_class_select, name='view_timetable_class_select'),
    path('view/timetable/professor/', timetable.view_timetable_professor, name='view_timetable_professor'),
    path('view/timetable/professor/<shift>/', timetable.view_timetable_professor_select, name='view_timetable_professor_select'),

    path('changes/professor/', changes.changes_professor, name='changes_professor'),
    path('changes/subject/', changes.changes_subject, name='changes_subject'),
    path('approve/changes/professor/', changes.approve_changes_professor, name='approve_changes_professor'),
    path('approve/changes/subject/', changes.approve_changes_subject, name='approve_changes_subject'),
]
