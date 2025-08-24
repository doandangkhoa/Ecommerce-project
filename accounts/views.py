from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# for email vertification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()
            
            # user activation
            current_site = get_current_site(request)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid' : uid,
                'token' : token
            })
            send_message = EmailMessage(email_subject, message, to=[email])
            messages.success(request, 'Registration was successful !')
            return redirect('register')
        else:
            messages.error(request, "There was an error with your registration")
    else:
        form = RegistrationForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    username = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            username = user.username
            messages.success(request, 'You are logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'email or password is incorrect')
    context = {'username' : username}
    return render(request, 'accounts/login.html', context)

@login_required(login_url = 'login')
def logoutPage(request):
    logout(request)
    messages.success(request, 'You are logged out!')
    return redirect('home')