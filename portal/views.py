from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Q
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import AskForm, AnswerForm, CommentForm
from .models import Question, Candidate, Comment, User
from . import choices


def candidate_detail_view(request, pk):
    try:
        candidate = Candidate.objects.get(id=pk)
        d = {
            'candidate': candidate,
            'comment_form': CommentForm(),
            'question_form': AskForm(),
            'questions': Question.objects.filter(asked_to=candidate).filter(approved=True).order_by('-asked_on')
        }
        print(d)
    except:
        d = {'candidate': None}
    return render(request, 'candidate_detail.html', d)


class UpvoteAPIToggle(APIView):

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = User.objects.get(email=request.session['user']['email'])
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if request.session['user']['is_authenticated']:
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

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = User.objects.get(email=request.session['user']['email'])
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if request.session['user']['is_authenticated']:
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


class UpvoteAPIToggleComment(APIView):

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Comment, pk=pk)
        user = User.objects.get(email=request.session['user']['email'])
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if request.session['user']['is_authenticated']:
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


class DownvoteAPIToggleComment(APIView):

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Comment, pk=pk)
        user = User.objects.get(email=request.session['user']['email'])
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if request.session['user']['is_authenticated']:
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


class ApproveAPIToggle(APIView):

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = User.objects.get(email=request.session['user']['email'])
        updated = False
        if request.session['user']['is_authenticated']:
            if user.junta.role == choices.ELECTION_COMMISSION:
                if not obj.approved:
                    updated = True
                    obj.approved = True
                    obj.approved_by = user.junta
                    obj.save()
        data = {
            'updated': updated,
        }
        return Response(data)


class ApproveAPIToggleComment(APIView):

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Comment, pk=pk)
        user = User.objects.get(email=request.session['user']['email'])
        updated = False
        if request.session['user']['is_authenticated']:
            if user.junta.role == choices.ELECTION_COMMISSION:
                if not obj.approved:
                    updated = True
                    obj.approved = True
                    obj.approved_by = user.junta
                    obj.save()
        data = {
            'updated': updated,
        }
        return Response(data)


class DeleteQuestionAPIToggle(APIView):

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = User.objects.get(email=request.session['user']['email'])
        updated = False
        if request.session['user']['is_authenticated']:
            if user.junta.role == choices.ELECTION_COMMISSION:
                updated = True
                for comment in obj.comments.all():
                    comment.delete()
                obj.delete()
        data = {
            'updated': updated,
        }
        return Response(data)


class DeleteCommentAPIToggle(APIView):

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Comment, pk=pk)
        user = User.objects.get(email=request.session['user']['email'])
        updated = False
        if request.session['user']['is_authenticated']:
            if user.junta.role == choices.ELECTION_COMMISSION:
                updated = True
                obj.delete()
        data = {
            'updated': updated,
        }
        return Response(data)


class SortQuestionsAPI(APIView):

    def get(self, request, *args, **kwargs):
        data = {}
        # qs = self.get_queryset()
        sort_by = request.GET.get('sort_by')
        sort_on = request.GET.get('sort_on')
        data[sort_by] = sort_by
        data[sort_on] = sort_on
        user_ = User.objects.get(email=request.session['user']['email'])
        if sort_on == "my-questions":
            user = user_.junta.candidate.all()[0]
            print("candidate =", user)
            questions = Question.objects.filter(asked_to=user).filter(approved=True)
        else:
            user = user_.junta
            if user_.junta.role == "Candidate":
                questions = Question.objects.filter(~Q(asked_to=user_.junta.candidate.all()[0])).filter(approved=True)
            else:
                questions = Question.objects.filter(approved=True)

        if sort_by=='upvotes':
            questions = sorted(questions, key = lambda t: t.upvotes.count(), reverse = True)
        else:
            questions = questions.order_by('-asked_on')

        data['html_questions'] = render_to_string(
            template_name='questions.html',
            context={'questions': questions,
                     'user': user_.junta,
                     'question_type': sort_on,
                     'comment_form': CommentForm()},
            request=request
        )

        return Response(data)


def index(request):
    question_form = AskForm()
    comment_form = CommentForm()
    d = {'question_form': question_form, 'comment_form': comment_form}
    if request.session['user']['is_authenticated']:
        d['is_authenticated'] = True
        user = User.objects.get(email=request.session['user']['email'])
        d['user'] = user
        if user.junta.role == choices.ELECTION_COMMISSION:
            unapproved_questions = Question.objects.filter(approved=False).order_by('-asked_on')
            unapproved_comments = Comment.objects.filter(approved=False).order_by('-commented_on')
            approved_questions = Question.objects.filter(approved=True).order_by('-asked_on')
            d['unapproved_questions'] = unapproved_questions
            d['unapproved_comments'] = unapproved_comments
            d['role'] = 'admin'
        elif user.junta.role == choices.CANDIDATE:
            approved_questions = Question.objects.filter(approved=True)\
                                                 .filter(~Q(asked_to=user.junta.candidate.all()[0]))\
                                                 .order_by('-asked_on')
            my_questions = Question.objects.filter(asked_to=user.junta.candidate.all()[0])\
                                           .filter(approved=True)\
                                           .order_by('-asked_on')
            print(my_questions)
            d['my_questions'] = my_questions
        else:
            approved_questions = Question.objects.filter(approved=True).order_by('-asked_on')
    else:
        approved_questions = Question.objects.filter(approved=True).order_by('-asked_on')
    d['approved_questions'] = approved_questions
    if request.method == 'POST':
        if d['is_authenticated']:
            questionForm = AskForm(request.POST)
            if questionForm.is_valid():
                question = questionForm.save(commit=False)
                question.asked_by = user.junta
                question.save()
                questionForm.save_m2m()
                pass
            else:
                print(questionForm.errors)
            return HttpResponseRedirect(reverse('portal:index'))
        else:
            return HttpResponseRedirect(reverse('portal:login'))

    return render(request, 'index.html', d)


def load_candidates(request):
    position = request.GET.get('position')
    candidates = Candidate.objects.filter(position=position)
    return render(request, 'candidates_dropdown_list.html', {'candidates': candidates})


def answer_view(request, pk):
    question = Question.objects.get(pk=pk)
    answer_form = AnswerForm()
    user = User.objects.get(email=request.session['user']['email'])
    if question.answered:
        answer_form = AnswerForm({'answer': question.answer})

    d = {'question': question, 'answer_form': answer_form}

    if request.session['user']['is_authenticated']:
        d['is_authenticated'] = True

    if request.POST:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            question.answer = answer
            question.answered = True
            question.answered_on = timezone.now()
            question.save()
        else:
            print("AnswerForm POST Error: ", form.errors)
        return HttpResponseRedirect(reverse('portal:index'))

    return render(request, 'answer.html', d)


def comment_view(request, pk):
    question = Question.objects.get(pk=pk)
    comment_form = CommentForm()
    user = User.objects.get(email=request.session['user']['email'])
    d = {'question': question, 'comment_form': comment_form}

    if request.session['user']['is_authenticated']:
        d['is_authenticated'] = True

    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_by = user.junta
            comment.question = question
            comment.comment = form.cleaned_data['comment']
            comment.commented_on = timezone.now()
            comment.save()
            form.save_m2m()
            pass
        else:
            print("CommentForm POST Error: ", form.errors)
        return HttpResponseRedirect(reverse('portal:index'))

    return render(request, 'comment.html', d)


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
