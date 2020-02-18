from django.shortcuts import render
from portal.models import Hostel


def chart(request):
    context = {
        'hostels': Hostel.objects.all(),
        'nbar': 'stats'
    }
    return render(request, 'stats/111.html', context)
