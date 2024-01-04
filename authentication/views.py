# authentication/views.py
from django.shortcuts import render, redirect ,  get_object_or_404
from django.contrib.auth import authenticate, login , logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        profile_picture = request.FILES.get('profile_picture')  # Use request.FILES

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'authentication/signup.html', {'error': 'Username is already taken'})

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
            return render(request, 'authentication/signup.html', {'error': 'Passwords do not match'})

    return render(request, 'authentication/signup.html')

def user_login(request):
    error_message = None

    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']

        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        user_by_email = CustomUser.objects.filter(email=username_or_email).first()
        if user_by_email is not None and user_by_email.check_password(password):
            login(request, user_by_email)
            return redirect('home')

        error_message = 'Invalid login credentials'

    return render(request, 'authentication/login.html', {'error': error_message})

@login_required
def home(request):
    recent_users_list = CustomUser.objects.exclude(id=request.user.id).order_by('-date_joined')

    paginator = Paginator(recent_users_list,3)
    page = request.GET.get('page')

    try:
        recent_users = paginator.page(page)
    except PageNotAnInteger:
        recent_users = paginator.page(1)
    except EmptyPage:
        recent_users = paginator.page(paginator.num_pages)

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
    user = request.user

    first_name = user.first_name
    last_name = user.last_name
    profile_picture = user.profile_picture 

    context = {
        'user': user,
        'first_name': first_name,
        'last_name': last_name,
        'profile_picture': profile_picture,
    }

    return render(request, 'authentication/profile_page.html', context)

@login_required
def view_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    first_name = user.first_name
    last_name = user.last_name
    profile_picture = user.profile_picture

    # Context data
    context = {
        'user': user,
        'first_name': first_name,
        'last_name': last_name,
        'profile_picture': profile_picture,
    }

    return render(request, 'authentication/view_profile.html', context)


