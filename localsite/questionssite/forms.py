from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from django import forms

from .models import Answers, Questions

User = get_user_model()


class AnswersForm(forms.ModelForm):

    def clean(self):
        check_correct_answers = 0
        quanty_answers = int(self.data.get('answers_set-TOTAL_FORMS'))
        for right_id in range(quanty_answers):
            if self.data.get(f'answers_set-{right_id}-correct'):
                check_correct_answers += 1
        if check_correct_answers == 0:
            raise ValidationError("Выберите верный ответ")
        elif quanty_answers == check_correct_answers:
            raise ValidationError("Нельзя выбирать все ответы правильными")

        return self.cleaned_data

    class Meta:
        model = Answers
        fields = ["title", "correct"]


class RegisterCustomForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "form-control",
            "placeholder": "*******"
        })
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "*******"
            })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username',
            'password1',
            'password2'
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Username"
                }
            )}


class LoginCustomForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Username"
            }
        ))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
                "placeholder": "*******"
            })
    )


class QuestionForm(forms.ModelForm):
    correct = forms.BooleanField(required=False)

    class Meta:
        model = Answers
        fields = ["correct"]
