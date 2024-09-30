from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import All_knifes, Grinding_data, Honing_data




class All_knifesForm_step1(forms.ModelForm):
    class Meta:
        model = All_knifes
        exclude = ['carbon', 'CrMoV', 'angle', 'honing_add', 'category']


class All_knifesForm_step2(forms.ModelForm):
    class Meta:
        model = All_knifes
        exclude = ['brand', 'series', 'steel', 'angle', 'honing_add', 'category']


class Grinding_dataForm(forms.ModelForm):
    class Meta:
        model = Grinding_data
        exclude = ['USH']


class Honing_dataForm(forms.ModelForm):
    class Meta:
        model = Honing_data
        exclude = ['FVB_H']

# форма для регистрации нового пользователя
class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True, ):
        user = super().save(commit=False)
        user.is_active = False # активация устанавливается True после подтверждения верефикации по ссылке
        if commit:
            user.save()
        return user

# форма для редактирования аккаунта
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
