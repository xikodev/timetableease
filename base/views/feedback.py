from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings as confsettings
from ..decorators import group_required


@group_required(redirect_page='waiting')
@login_required(login_url='login')
def feedback(request):
    args = {
        'feedback_subjects': ['Greska u aplikaciji', 'Prijedlog/Zahtjev', 'Ostalo']
    }

    if request.method == 'POST':
        feedback_subject = request.POST.get('feedback_subject')
        feedback_comment = request.POST.get('feedback_comment')
        feedback_file = request.FILES['feedback_file']
        mail = EmailMessage(feedback_subject, f'FROM: {request.user.email}\n\n{feedback_comment}', confsettings.EMAIL_HOST_USER, [confsettings.EMAIL_HOST_USER])
        mail.attach(feedback_file.name, feedback_file.read(), feedback_file.content_type)
        mail.send()
        return redirect('feedback_thanks')

    return render(request, 'feedback/feedback.html', args)


@group_required(redirect_page='waiting')
@login_required(login_url='login')
def feedback_thanks(request):
    return render(request, 'feedback/feedback_thanks.html')
