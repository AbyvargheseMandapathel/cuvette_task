# authentication/views.py
from django.shortcuts import render, redirect ,  get_object_or_404
from django.contrib.auth import authenticate, login , logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        profile_picture = request.FILES.get('profile_picture')  # Use request.FILES

         # Validate unique email
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'authentication/signup.html', {'error': 'Username is already taken'})

        # Validate unique email
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'authentication/signup.html', {'error': 'Email is already taken'})

        if password == confirm_password:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                profile_picture=profile_picture,
            )
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

@login_required
def home(request):
    # Fetch 5 recently added users excluding the current user
    recent_users = CustomUser.objects.exclude(id=request.user.id).order_by('-date_joined')[:5]
    user = request.user
    profile_picture = user.profile_picture 

    return render(request, 'authentication/home.html', {
        'username': request.user.username,
        'email': request.user.email,
        'recent_users': recent_users,
        'profile_picture': profile_picture,
    })

@login_required    
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile_page(request):
    # Assuming you have a user object associated with the request
    user = request.user

    # Additional user details
    first_name = user.first_name
    last_name = user.last_name
    profile_picture = user.profile_picture 

    # Context data
    context = {
        'user': user,
        'first_name': first_name,
        'last_name': last_name,
        'profile_picture': profile_picture,
        # Add more context variables if needed
    }

    return render(request, 'authentication/profile_page.html', context)

@login_required
def view_profile(request, user_id):
    # Retrieve the user based on the user_id
    user = get_object_or_404(CustomUser, id=user_id)

    # Additional user details
    first_name = user.first_name
    last_name = user.last_name
    profile_picture = user.profile_picture

    # Context data
    context = {
        'user': user,
        'first_name': first_name,
        'last_name': last_name,
        'profile_picture': profile_picture,
        # Add more context variables if needed
    }

    return render(request, 'authentication/view_profile.html', context)


