from django import forms
from users.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['link','avatar', 'gender']
