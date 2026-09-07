from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# ================= REGISTER =================

def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        # Empty fields

        if not username or not email or not password or not confirm_password:

            messages.error(
                request,
                'Please fill all fields.'
            )

            return redirect('register')


        # Password match

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')


        # Username already exists

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')


        # Email already exists

        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                'Email is already registered.'
            )

            return redirect('register')


        # Create user

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        # Automatically login after registration

        login(request, user)


        messages.success(
            request,
            f'Welcome to Programming Blog, {user.username}! 🎉'
        )


        return redirect('blog:home')


    # IMPORTANT:
    # login.html/register.html templates folder ke andar direct hain

    return render(request, 'register.html')


# ================= LOGIN =================

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(request, user)


            messages.success(
                request,
                f'Welcome back, {user.username}! 👋'
            )


            # Agar kisi protected page se login par aaye hain

            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)


            return redirect('blog:home')


        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

            return redirect('login')


    # IMPORTANT:
    # login.html templates folder ke andar direct hai

    return render(request, 'login.html')


# ================= LOGOUT =================

def logout_view(request):

    logout(request)


    messages.success(
        request,
        'You have been logged out successfully.'
    )


    return redirect('/')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# ================= PROFILE =================

def profile_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(
        request,
        'accounts/profile.html',
        {
            'profile_user': request.user
        }
    )


# ================= MY BLOGS =================

def my_blogs_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    from blog.models import Blog

    blogs = Blog.objects.filter(
        author=request.user.username
    ).order_by('-created_at')

    return render(
        request,
        'accounts/my_blogs.html',
        {
            'blogs': blogs
        }
    )