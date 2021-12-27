from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import get_user_model, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib import messages
import uuid

User= get_user_model()

def token_creater():
    return uuid.uuid4()

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegistrationForm

    def form_valid(self, form):
        token = token_creater()
        email = form.instance.email
        form.instance.token = token
        send_email(email,token)
        return super(RegisterView,self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request,"Your account created successfully get your email and activete")
        return reverse('login')

def loginUser(request):
    form = UserLoginForm()

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_obj = User.objects.get(email=email)
            if user_obj.is_active == True:
                login(request,user_obj)
                return redirect('index')
            else:
                messages.error(request,'Your accoun is not activate')
                return redirect('login')

    context = {
        'form':form
    }
    return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def activate(request,token):
    user = User.objects.get(token=token)
    user.is_active = True
    user.save()
    return redirect('login')

def send_email(email,token):
    message = f"You can activate your account with http://127.0.0.1:8000/accounts/activate/{token}/ this link"
    subject = "Activate your ToDoApp account"
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject,message,from_email,[email])

