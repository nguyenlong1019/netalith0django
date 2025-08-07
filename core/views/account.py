from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required 
from core.models.user import User 


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index_view')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, 'Please enter both email and password!')
            return redirect('login_view')
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.error(request, "Email or password incorrect!")
            return redirect('login_view')
        login(request, user)
        next_url = request.GET.get('next') or 'index_view'
        return redirect(next_url)

    return render(request, 'core/login.html', status=200)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index_view')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if not email or not password or not confirm_password:
            messages.error(request, 'Please enter email, password and confirm password!')
            return redirect('register_view')
        if password != confirm_password:
            messages.error(request, 'Password and confirm password does not match!')
            return redirect('register_view')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!, Please use another email!.")
            return render(request, 'core/register.html', status=200) 
        user = User.objects.create_user(
            email=email,
            password=password
        )
        login(request, user)
        return redirect('index_view')
    return render(request, 'core/register.html', status=200)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('index_view')

