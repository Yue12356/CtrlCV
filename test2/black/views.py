from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from black.static.black.data import json_test
from black.static.black.data import db_load
import json,datetime
# from rest_framework.views import APIView
# from rest_framework.response import Response

from .models import PlayerInfo
from .forms import PlayerForm
import aiofiles,os,asyncio

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


result = ''
async def aload_json():
     print("\n\n\n\n\n\loading file")
     global result
     async with aiofiles.open(os.getcwd()+'\\'+'black\\result.json', mode='r', encoding='utf8') as op:
         async for l in op:
             result+=l
     print('Done')
    #  return result


def base(request):
    return render(request,'black/base.html',{})

def home(request):

    return render(request,'black/home.html',{})

def about(request):

    return render(request, 'black/about.html',{})

def services(request):

    return render(request, 'black/services.html',{})
def team(request):
    return render(request, 'black/team.html')
def game2(request):
    return render(request, 'black/game2.html')

def player_query(request):
    # print(request.GET['name'])
    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
        form = PlayerForm(request.POST)
    # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlayerForm()
    # return HttpResponseRedirect('../player')
    return render(request, 'black/player2.html', {'form': form})


def player(request):
    print('\n\n\n\n\n\n')
    # print(context)
    name = request.GET['name']
    date_range = request.GET['date_range']
    context = {
        'name':name,
        'date_range':int(date_range),
        'result':[],
        'lables':[],
        'point':[],
        'two_hit':[],
        'three_hit':[],
        'penalty_hit':[],
        'bord':[],
        'sup':[],
        'ST':[],
        }
    # print(name)
    query_set = PlayerInfo.objects.filter(player_name__exact=name)
    # times = list(result[name].keys())
    # print(times)
    try:
        if context['date_range']<=0 or context['date_range']>30 or len(query_set)==0:
            form = PlayerForm()
            print(query_set)
            if date_range:
                messages.success(request,"不存在！")
            return render(request, 'black/player2.html', {'form': form})
        for n in range(len(query_set))[-context['date_range']:]:
            # pritn()
            context['lables'].append(json.dumps(query_set[n].game_time,cls=DateEncoder))
            context['point'].append(json.dumps(query_set[n].point))
            context['two_hit'].append(json.dumps(query_set[n].two_hit))
            context['three_hit'].append(json.dumps(query_set[n].three_hit))
            context['penalty_hit'].append(json.dumps(query_set[n].penalty_hit))
            context['bord'].append(json.dumps(query_set[n].bord))
            context['sup'].append(json.dumps(query_set[n].sup))
            context['result'].append(
                str(query_set[n].game_time)+
                ', 得分为 '+str(query_set[n].point)+
                ', 三分命中率 '+ str(query_set[n].three_rate)+
                ', 两分命中率 '+str(query_set[n].two_rate))
            # context['score'].append(result[name][game_time]['得分'])
    except():
        form = PlayerForm()
        return render(request, 'black/player2.html', {'form': form})
    # db_load.load()
    print(context['lables'])
    return render(request, 'black/player.html',context)

def chart_test(request):
    return render(request,'black/chart_test.html',context={})

# class ChartTest(APIview):
#     pass

# Create your views here.

'''
2019.6.30
    Database bounded! 
    Following works are: visualizing, formating, advanced searching(date, non-exact name, player link)
'''