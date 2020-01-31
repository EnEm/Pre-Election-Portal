from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AskForm
from .models import Question


class UpvoteAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = self.request.user
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if user.is_authenticated:
            updated = True
            if user.junta in obj.upvotes.all():
                obj.upvotes.remove(user.junta)
                upvote = -1
            else:
                if user.junta in obj.downvotes.all():
                    obj.downvotes.remove(user.junta)
                    downvote = -1
                obj.upvotes.add(user.junta)
                upvoteColor = "blue"
                upvote = 1

        data = {
            'updated': updated,
            'upvote': upvote,
            'downvote': downvote,
            'upvoteColor': upvoteColor,
            'downvoteColor': downvoteColor
        }
        return Response(data)


class DownvoteAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = self.request.user
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if user.is_authenticated:
            updated = True
            if user.junta in obj.downvotes.all():
                obj.downvotes.remove(user.junta)
                downvote = -1
            else:
                if user.junta in obj.upvotes.all():
                    obj.upvotes.remove(user.junta)
                    upvote = -1
                obj.downvotes.add(user.junta)
                downvoteColor = "red"
                downvote = 1

        data = {
            'updated': updated,
            'upvote': upvote,
            'downvote': downvote,
            'upvoteColor': upvoteColor,
            'downvoteColor': downvoteColor
        }
        return Response(data)


def index(request):
    question_form = AskForm()
    questions = Question.objects.all().order_by('asked_on')
    d = {'questions': questions, 'question_form': question_form}

    if request.user.is_authenticated:
        d['is_authenticated'] = True
        d['user'] = request.user.junta

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
