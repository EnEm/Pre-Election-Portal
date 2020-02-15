from django.shortcuts import render
from django.http import HttpResponse
from portal.models import Hostel

def chart(request):
    
    dataSource = {}
    dataSource['data'] = []
    for key in Hostel.objects.all():
      data = {}
      data['y'] = 100*key.no_of_votes/key.total_residents
      data['label'] = key.name
      dataSource['data'].append(data)

    dicti = {'output': dataSource['data']}
    return render(request,'stats/111.html',context = dicti )