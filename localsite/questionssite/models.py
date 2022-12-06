from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    last_login = None
    first_name = None
    last_name = None
    date_joined = None

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class CategoriesQuestion(models.Model):
    title = models.CharField(max_length=300, verbose_name="Название теста")
    description = models.CharField(max_length=1200, verbose_name="Описание теста")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Questions(models.Model):
    title = models.CharField(max_length=450, verbose_name="Текст вопроса")
    cat_title = models.ForeignKey("CategoriesQuestion", on_delete=models.SET_DEFAULT, default="Отдельная категория")
    visible = models.BooleanField(default=False, verbose_name="Отображение вопроса")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answers(models.Model):
    question_title = models.ForeignKey("Questions", on_delete=models.CASCADE)
    title = models.CharField(max_length=900, verbose_name="Ответ")
    correct = models.BooleanField(default=False, verbose_name="Верный ответ")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class UserQuestionsCheck(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    title_test = models.ForeignKey("CategoriesQuestion", on_delete=models.CASCADE)
    quantity_answer = models.PositiveIntegerField(verbose_name="Отвеченно", default=0)
    quantity_right_answer = models.PositiveIntegerField(verbose_name="Верные ответы", default=0)
