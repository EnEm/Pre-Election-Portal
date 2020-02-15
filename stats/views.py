from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from portal.models import Hostel
from portal.forms import UpdateStatsForm
from django.views.generic import UpdateView

def chart(request):
    
    dataSource = {}
    dataSource['data'] = []
    for key in Hostel.objects.all():
      data = {}
      data['y'] = 100*key.no_of_votes/key.total_residents
      data['label'] = key.name
      data['count'] = key.no_of_votes
      data['residents'] = key.total_residents
      dataSource['data'].append(data)

    dicti = {'output': dataSource['data']}
    return render(request,'stats/111.html',context = dicti )

def update(request):
  if request.method == "POST":
    form = UpdateStatsForm(request.POST)  
    if form.is_valid():
      form.save()
    return render(request,'stats/update.html',{'form': form})
  else:
    form = UpdateStatsForm()
    return render(request,'stats/update.html',{'form': form})
# class update(UpdateView):
#     model = Hostel
#     form_class = UpdateStatsForm
#     template_name = 'stats/update.html'
