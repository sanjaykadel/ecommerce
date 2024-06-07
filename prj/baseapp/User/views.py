from django.shortcuts import render, redirect
from .forms import UserSignUpForm , LoginForm
from django.contrib.auth import authenticate, login , logout ,get_user_model
from baseapp.views import get_common_context

def logout_view(request):
    logout(request)
    request.session.flush()  # Clear the current session data
    return redirect('login')  # Replace 'login' with the URL name of your login page

def signup(request):
    context = get_common_context()
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful signup
            login(request, user)
            return redirect('login')  # Replace 'home' with the URL name of your desired page
    else:
        form = UserSignUpForm()
    context['form'] = form
    return render(request, 'register/signup.html', context)


def login_view(request):
    context = get_common_context()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('about')  # Replace 'home' with the URL name of your desired page
            except User.DoesNotExist:
                form.add_error('email', 'Invalid email or password')
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'register/login.html', context)