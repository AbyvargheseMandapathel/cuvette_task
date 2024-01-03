# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            # Handle password mismatch
            return render(request, 'authentication/signup.html', {'error': 'Passwords do not match'})

    return render(request, 'authentication/signup.html')

def user_login(request):
    error_message = None

    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']

        # Authenticate user by either username or email
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            # Login successful, redirect to home
            login(request, user)
            return redirect('home')

        # If authentication by username fails, try by email
        user_by_email = CustomUser.objects.filter(email=username_or_email).first()
        if user_by_email is not None and user_by_email.check_password(password):
            # Login successful, redirect to home
            login(request, user_by_email)
            return redirect('home')

        # Set error message for invalid login
        error_message = 'Invalid login credentials'

    return render(request, 'authentication/login.html', {'error': error_message})

def home(request):
    if request.user.is_authenticated:
        return render(request, 'authentication/home.html', {'username': request.user.username})
    else:
        return redirect('login')
