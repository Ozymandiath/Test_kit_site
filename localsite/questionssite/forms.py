from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

from .models import Answers

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
