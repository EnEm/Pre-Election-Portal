from django.shortcuts import render
from django.utils.decorators import method_decorator
from portal.models import Hostel
from portal.forms import UpdateStatsForm
from django.views.generic import CreateView, UpdateView, DeleteView
from .decorators import user_is_admin
from portal.models import User
from portal.choices import ELECTION_COMMISSION


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
    return render(request, 'stats/hostel_stats.html', context=dicti)


@user_is_admin
def update(request):
    if request.method == "POST":
        form = UpdateStatsForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'stats/update.html', {'form': form})
    else:
        form = UpdateStatsForm()
        return render(request, 'stats/update.html', {'form': form})


@method_decorator(user_is_admin, name='dispatch')
class HostelCreateview(CreateView):
    model = Hostel
    fields = ['name', 'total_residents', 'no_of_votes']
    template_name = 'stats/update.html'
    success_url = '/statistics'


@method_decorator(user_is_admin, name='dispatch')
class HostelUpdateview(UpdateView):
    model = Hostel
    fields = ['name', 'total_residents', 'no_of_votes']
    template_name = 'stats/update.html'
    success_url = '/statistics'


@method_decorator(user_is_admin, name='dispatch')
class hostelDeleteview(DeleteView):
    model = Hostel
    template_name = 'stats/hosteldelete.html'
    success_url = '/statistics'
