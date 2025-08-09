from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from core.models.assistant import AssistantLog 


def index_view(request):
    return render(request, 'core/index.html', status=200)


@login_required(login_url='/login')
def ai_assistant_view(request):
    messages = AssistantLog.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'core/ai-assistant.html', {'messages': messages}, status=200)