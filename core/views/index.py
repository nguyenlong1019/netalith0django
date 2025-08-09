from django.shortcuts import render 
from django.contrib.auth.decorators import login_required


def index_view(request):
    return render(request, 'core/index.html', status=200)


@login_required(login_url='login')
def ai_assistant_view(request):
    return render(request, 'core/ai-assistant.html', status=200)