from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import CustomUser, MinimalModel

class SignUpForm(UserCreationForm):
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='オプション',
        label='苗字'
    )

    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='オプション',
        label='名前'
    )

    email = forms.EmailField(
        max_length=254,
        help_text='必須　有効なメールアドレスを入力してください',
        label='Eメールアドレス'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2')

class ThingForm(forms.ModelForm):
    class Meta:
        model = MinimalModel
        fields = ('title', 'buy_reason', 'obj_image', 'buy_date', 'buy_price')