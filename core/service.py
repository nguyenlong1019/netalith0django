import requests 
from django.conf import settings 
from core.utils import get_user 
from core.models.assistant import AssistantLog 


API_KEY = settings.OPEN_API_API_SECRET_KEY


class ChatGPTService:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.messages = []
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }
        self.url = 'https://api.openai.com/v1/chat/completions'

    
    def build_base_messages(self):
        user = get_user(self.user_id)
        if not user:
            return False, 'user invalid'
        messages = AssistantLog.objects.filter(user=user).order_by('-created_at')
        if messages:
            for m in messages:
                self.messages.extend({
                    {"role": "user", "content": m.user_msg},
                    {"role": "assistant", "content": m.assistant_msg}
                })


    def call_openai(self, user_content):
        data = {
            "model": "gpt-5-nano",
            "temperature": 0.8,
            "messages": self.messages + [{"role": "user", "content": user_content}]
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        return response 
    

    def save_log(self, user_msg, assistant_msg, data):
        AssistantLog.objects.create(
            user=get_user,
            user_msg=user_msg,
            assistant_msg=assistant_msg,
            cid=data.get('id'),
            prompt_tokens = data['usage']['prompt_tokens'],
            completion_tokens = data['usage']['completion_tokens'],
            total_tokens = data['usage']['prompt_tokens']
        )
    
    
    def run(self, params = None):
        self.build_base_messages()
        user_content = params.get('user_content')
        if not user_content:
            return False, 'User content invalid'
        response = self.call_openai(user_content)
        if response.status_code == 200:
            data = response.json()
            assistant_msg = data["choices"][0]["message"]["content"]
            self.save_log(user_content, assistant_msg, data)
            return True, assistant_msg 
        err_res = {
            'status_code': response.status_code,
            'json': response.json(),
            'text': response.text
        }
        return False, err_res
