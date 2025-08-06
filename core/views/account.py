from django.shortcuts import render 


def login_view(request):
    return render(request, 'core/login.html', status=200)


def register_view(request):
    return render(request, 'core/register.html', status=200)


def logout_view(request):
    pass 

