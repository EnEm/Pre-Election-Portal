from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import RedirectView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AskForm
from .models import Question


class UpvoteAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        obj = get_object_or_404(Question, id=self.kwargs.get("pk"))
        user = self.request.user

        if user.is_authenticated:
            if user.junta in obj.upvotes.all():
                obj.upvotes.remove(user.junta)
            else:
                if user.junta in obj.downvotes.all():
                    obj.downvotes.remove(user.junta)
                obj.upvotes.add(user.junta)

        data = {

        }
        return Response(user)


class UpvoteToggleView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Question, id=self.kwargs.get("pk"))
        user = self.request.user

        if user.is_authenticated:
            if user.junta in obj.upvotes.all():
                obj.upvotes.remove(user.junta)
            else:
                if user.junta in obj.downvotes.all():
                    obj.downvotes.remove(user.junta)
                obj.upvotes.add(user.junta)
        return reverse('portal:index')


class DownvoteToggleView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Question, id=self.kwargs.get("pk"))
        user = self.request.user

        if user.is_authenticated:
            if user.junta in obj.downvotes.all():
                obj.downvotes.remove(user.junta)
            else:
                if user.junta in obj.upvotes.all():
                    obj.upvotes.remove(user.junta)
                obj.downvotes.add(user.junta)
        return reverse('portal:index')


def index(request):
    question_form = AskForm()
    questions = Question.objects.all().order_by('asked_on')
    d = {'questions': questions, 'question_form': question_form}

    if request.user.is_authenticated:
        d['is_authenticated'] = True

    if request.method == 'POST':
        if d['is_authenticated']:
            questionForm = AskForm(request.POST)
            if questionForm.is_valid():
                question = questionForm.save(commit=False)
                question.asked_by = request.user.junta
                question.save()
                pass
            else:
                print(questionForm.errors)
            return render(request, 'index.html', d)
        else:
            return HttpResponseRedirect(reverse('portal:login'))

    return render(request, 'index.html', d)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('portal:index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Wrong: {} {}".format(username, password))
            return HttpResponse("Invalid Login Details")
    else:
        return render(request, 'login.html')


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("portal:index"))
