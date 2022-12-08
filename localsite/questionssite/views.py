from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from questionssite.forms import RegisterCustomForm, LoginCustomForm, QuestionForm
from questionssite.models import CategoriesQuestion, Questions, UserQuestionsCheck


class TableListTest(ListView):
    template_name = "questionssite/table_test.html"
    model = CategoriesQuestion
    context_object_name = "cat_test"


class DetailsTest(View):
    template_name = "questionssite/detail.html"
    form_class = QuestionForm

    def get(self, request, pk1, pk2=None):
        question = Questions.objects.filter(cat_title=pk1)
        check_user_result = UserQuestionsCheck.objects.filter(title_test=pk1)
        if not check_user_result.count() and not pk2:
            question = question.get(pk=question.first().pk)
        elif not check_user_result.count() and pk2:
            question = question.get(pk=question.first().pk)
        elif check_user_result.get().quantity_answer < question.count():
            question = question.get(pk=question[check_user_result.get().quantity_answer].pk)
        else:
            return redirect("result", pk1)

        context = {
            "details": question,
            "cat_id": pk1,
            "form": self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk1, pk2):
        form = self.form_class(request.POST)
        id_list_answer = []
        right_id_answer = []
        if form.is_valid():
            answers_list = Questions.objects.get(pk=pk2).answers_set.all()
            for answer in answers_list:
                if form.data.get(f"answer-{answer.pk}"):
                    id_list_answer.append(int(form.data.get(f"answer-{answer.pk}")))
            right_answers = Questions.objects.get(pk=pk2).answers_set.filter(correct=True)
            for answer in right_answers:
                right_id_answer.append(answer.pk)
            user_check_question = UserQuestionsCheck.objects.filter(Q(user=request.user) & Q(title_test=pk1))
            if user_check_question.count():
                id_verified = user_check_question.get().quantity_answer + 1
                count_right_answer = user_check_question.get().quantity_right_answer
            else:
                id_verified = 1
                count_right_answer = 0
            category_for_user = CategoriesQuestion.objects.get(pk=pk1)
            if id_list_answer == right_id_answer:
                UserQuestionsCheck.objects.update_or_create(
                    user=request.user,
                    title_test=category_for_user,
                    defaults={'quantity_answer': id_verified,
                              'quantity_right_answer': count_right_answer + 1
                              }
                )
            else:
                UserQuestionsCheck.objects.update_or_create(
                    user=request.user,
                    title_test=category_for_user,
                    defaults={'quantity_answer': id_verified,
                              'quantity_right_answer': count_right_answer
                              }
                )
            question = Questions.objects.filter(Q(cat_title=pk1) & Q(pk__gt=pk2))
            if question.count():
                for question_next in question:
                    return redirect("pass", pk1, question_next.pk)
            else:
                return redirect("result", pk1)


class ResultTest(View):
    template_name = "questionssite/result.html"

    def get(self, request, pk):
        user_info = UserQuestionsCheck.objects.filter(title_test=pk)

        if user_info.count():
            context = {
                "right_answer": user_info.get().quantity_right_answer,
                "not_right_answer": user_info.get().quantity_answer - user_info.get().quantity_right_answer,
                "percent_right": (user_info.get().quantity_right_answer / user_info.get().quantity_answer) * 100
            }
            return render(request, self.template_name, context)
        else:
            return redirect("home")


class RegisterUser(View):
    form_class = RegisterCustomForm
    template_name = "questionssite/register.html"

    def get(self, request):
        context = {
            "form": self.form_class()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password2")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
        else:
            return render(request, self.template_name, {"form": form})


class UserLogin(LoginView):
    form_class = LoginCustomForm
    template_name = "questionssite/login.html"
    next_page = "home"
