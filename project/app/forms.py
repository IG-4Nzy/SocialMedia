from django import forms
from django.contrib.auth.models import User
from .models import socialmedia
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django import forms
from django.contrib.auth import get_user_model, update_session_auth_hash


class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}), required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        if password:
            user.set_password(password)
            update_session_auth_hash(self.request, user)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user
    
class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)