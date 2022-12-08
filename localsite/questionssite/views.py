from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from questionssite.forms import RegisterCustomForm, LoginCustomForm
from questionssite.models import CategoriesQuestion, Answers, Questions


class TableListTest(ListView):
    template_name = "questionssite/table_test.html"
    model = CategoriesQuestion
    context_object_name = "cat_test"
    # def get(self, request):
    #     context = {
    #         "test_suite": Questions.objects.all(),
    #     }
    #     return render(request, self.template_name, context)

class DetailsTest(DetailView):
    pass

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