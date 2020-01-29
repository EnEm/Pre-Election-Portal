from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from . import forms


def index(request):
    question_form = forms.AskForm()

    d = {'question_form': question_form}

    if request.user.is_authenticated:
        print("Logged In")
        d['is_authenticated'] = True
        return render(request, 'index.html', d)
    return render(request, 'index.html', d)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                print("Eureka")
                return HttpResponseRedirect(reverse('portal:index'))
            else:
                print("Inactive")
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
