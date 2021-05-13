from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models.fields.files import ImageField
from .models import CustomUser, MinimalModel, ThingStatus
import datetime

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
        help_text='有効なメールアドレスを入力してください',
        label='Eメールアドレス'
    )

    image = forms.ImageField(
        label = "ユーザー画像",
        help_text="オプション"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'last_name', 'first_name', 'image', 'email', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        label='ユーザー画像',
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'last_name', 'first_name', 'email', 'image', 'password')

class ThingForm(forms.ModelForm):
    buy_date = forms.DateField(
        initial=datetime.datetime.now(),
        help_text='年-月-日の形式で入力をしてください。',
        label="購入日"
    )

    buy_price = forms.IntegerField(
        initial=0,
        help_text="0以上の整数を入力してください。",
        label="購入金額"
    )

    status = forms.ModelChoiceField(
        queryset=ThingStatus.objects.all(),
        initial=1,
        help_text="物についての感想を入力してください。",
        label="物の状況"
    )

    class Meta:
        model = MinimalModel
        fields = ('title', 'buy_reason', 'obj_image', 'buy_date', 'buy_price', 'status')

class ThingUpdateForm(forms.ModelForm):
    obj_image = forms.ImageField(
        label='モノの画像',
    )
    class Meta:
        model = MinimalModel
        fields = ('title', 'buy_reason', 'sell_reason' , 'obj_image', 'buy_date', 'buy_price', 'sell_price', 'status')