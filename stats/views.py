from django.shortcuts import render, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from portal.choices import ELECTION_COMMISSION
from portal.decorators import user_has_role
from portal.forms import UpdateStatsForm
from portal.models import Hostel
from portal.models import User


def chart(request):

    dataSource = dict()
    dataSource['data'] = []
    for key in Hostel.objects.all():
        data = dict()
        data['y'] = 100 * key.no_of_votes / key.total_residents
        data['label'] = key.name
        data['count'] = key.no_of_votes
        data['residents'] = key.total_residents
        data['id'] = key.id
        dataSource['data'].append(data)

    dicti = {'output': dataSource['data'], 'nbar': 'stats'}

    try:
        if request.session['user']['is_authenticated']:
            user = User.objects.get(email=request.session['user']['email'])
            if user.junta.role == ELECTION_COMMISSION:
                dicti['admin'] = True
    except KeyError:
        pass

    print(dicti)
    request.session['redirect_callback'] = reverse('stats:chart')
    return render(request, 'stats/hostel_stats.html', context=dicti)


@user_has_role(ELECTION_COMMISSION)
def update(request):

    dicti = dict()
    try:
        if request.session['user']['is_authenticated']:
            user = User.objects.get(email=request.session['user']['email'])
            if user.junta.role == ELECTION_COMMISSION:
                dicti['admin'] = True
    except KeyError:
        pass

    if request.method == "POST":
        form = UpdateStatsForm(request.POST)
        if form.is_valid():
            form.save()
        dicti['form'] = form
        return render(request, 'stats/update.html', dicti)
    else:
        form = UpdateStatsForm()
        dicti['form'] = form
        return render(request, 'stats/update.html', dicti)


@method_decorator(user_has_role(ELECTION_COMMISSION), name='dispatch')
class HostelCreateview(CreateView):
    model = Hostel
    fields = ['name', 'total_residents', 'no_of_votes']
    template_name = 'stats/update.html'
    success_url = '/statistics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.session['user']['is_authenticated']:
                user = User.objects.get(email=self.request.session['user']['email'])
                if user.junta.role == ELECTION_COMMISSION:
                    context['admin'] = True
        except KeyError:
            pass
        return context


@method_decorator(user_has_role(ELECTION_COMMISSION), name='dispatch')
class HostelUpdateview(UpdateView):
    model = Hostel
    fields = ['name', 'total_residents', 'no_of_votes']
    template_name = 'stats/update.html'
    success_url = '/statistics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.session['user']['is_authenticated']:
                user = User.objects.get(email=self.request.session['user']['email'])
                if user.junta.role == ELECTION_COMMISSION:
                    context['admin'] = True
        except KeyError:
            pass
        return context


@method_decorator(user_has_role(ELECTION_COMMISSION), name='dispatch')
class hostelDeleteview(DeleteView):
    model = Hostel
    template_name = 'stats/hosteldelete.html'
    success_url = '/statistics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.session['user']['is_authenticated']:
                user = User.objects.get(email=self.request.session['user']['email'])
                if user.junta.role == ELECTION_COMMISSION:
                    context['admin'] = True
        except KeyError:
            pass
        return context
