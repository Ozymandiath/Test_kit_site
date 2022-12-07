from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .forms import AnswersForm
from .models import Questions, Answers, CategoriesQuestion

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "is_active")
    list_display_links = ("id", "username")
    search_fields = ("id", "username")


class AnswersAdmin(admin.TabularInline):
    model = Answers
    extra = 0
    form = AnswersForm


@admin.register(Questions)
class AdminQuestion(admin.ModelAdmin):
    inlines = [
        AnswersAdmin,
    ]

class QuestionsAdmin(admin.StackedInline):
    model = Questions
    extra = 0


@admin.register(CategoriesQuestion)
class CategoriesQuestionAdmin(admin.ModelAdmin):
    inlines = [
        QuestionsAdmin,
    ]
