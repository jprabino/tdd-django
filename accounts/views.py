from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import auth,messages
# Create your views here.
from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)

    url = request.build_absolute_uri(reverse('login') + '?token=' +str(token.uid))
    message_body = f'Usa el siguiente link para loguearte:\n\n{url}'
    send_mail(
        'Tu link de logueo a Superlists',
        message_body,
        'noreply@superlists',
        [email],
    )
    messages.success(request, "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    # token = request.GET['token']
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
