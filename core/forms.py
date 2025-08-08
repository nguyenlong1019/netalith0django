from django import forms 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
from core.models.user import User 


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            "class": "vTextField"
        }
    ))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
        attrs={
            "class": "vTextField"
        }
    ))


    class Meta:
        model = User 
        fields = ('email', 'fullname')


    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don’t match")
        return p2
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Password')


    class Meta:
        model = User
        fields = ("email", "fullname", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
