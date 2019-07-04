from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import ListView
from black.static.black.data import json_test
from black.static.black.data import db_load
import json,datetime,prediction,string
# from rest_framework.views import APIView
# from rest_framework.response import Response

from .models import PlayerInfo,teamInfo
from .forms import PlayerForm,TeamForm
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
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('')
    else:
        form = TeamForm()
    return render(request, 'black/team.html',{'form':form})

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

def team_data(request):
    print('\n\n\n\n\n\n')
    # print(context)
    name = request.GET['teamName']
    date_range = request.GET['date_range']
    context = {
        'name':name,
        'date_range':int(date_range),
        'lables':[],
        'point':[],
        'two_hit':[],
        'three_hit':[],
        'penalty_hit':[],
        'bord':[],
        'miss':[],
        'winPercentage':[]
        }
    # print(name)
    query_set = teamInfo.objects.filter(team_name__exact=name)
    # times = list(result[name].keys())
    # print(times)
    try:
        if context['date_range']<=0 or context['date_range']>82 or len(query_set)==0:
            form = TeamForm()
            print(query_set)
            if date_range:
                messages.success(request,"不存在！")
            return render(request, 'black/team.html', {'form': form})
        win = 0 
        lose = 0
        for n in range(len(query_set))[-context['date_range']:]:
            # pritn()
            context['lables'].append(json.dumps(query_set[n].game_time,cls=DateEncoder))
            context['point'].append(json.dumps(query_set[n].point))
            context['two_hit'].append(json.dumps(query_set[n].two_hit))
            context['three_hit'].append(json.dumps(query_set[n].three_hit))
            context['penalty_hit'].append(json.dumps(query_set[n].penalty_hit))
            context['bord'].append(json.dumps(query_set[n].bord))
            context['miss'].append(json.dumps(query_set[n].miss))
            #print(json.dumps(query_set[n].wining))
            if json.dumps(query_set[n].wining)=='1':
                win+=1
            else:
                lose+=1
            # context['score'].append(result[name][game_time]['得分'])
        #print(win,lose)
        context['winPercentage'].append(win)
        context['winPercentage'].append(lose)
    except():
        form = TeamForm()
        return render(request, 'black/team.html', {'form': form})
    # db_load.load()
    print(context['lables'])
    print(context['winPercentage'])
    return render(request, 'black/team_data.html',context)

# def game2(request):
#     if request.method == 'POST':
#     # create a form instance and populate it with data from the request:
#         teamA_name = request.POST.get('team_A')
#         teamB_name = request.POST.get('team_B')
#         teamA={}
#         teamB={}
#         try:
#             for x in range(10):
#                 teamA[x]=splitString(request.POST.get("playerA_{}".format(x+1))
#                 teamB[x]=splitString(request.POST.get("playerB_{}".format(x+1))
#             teamAWin=prediction.predict(teamA,teamB)
#             return HttpResponseRedirect('')
#         except:
#             pass
#     return render(request, 'black/game2.html')

# def game2_ajax(request):
#     if request.is_ajax():
#         print('ajax request: ')
#     else:
#        print('not ajax request: ')
#     return render(request,'black/team_result.html',{})

    
def game2(request):
    #team_name="no team input"
    if request.method == 'POST':
        print("POST!!!")
        form = PlayerForm(request.POST)
        teamA={}
        teamB={}
        teamA_name = request.POST.get('team_A')
        teamB_name = request.POST.get('team_B')
        try:
            for x in range(10):
                teamA[x]=splitString(request.POST.get("playerA_{}".format(x+1)))
                teamB[x]=splitString(request.POST.get("playerB_{}".format(x+1)))
            print(teamA)
            print(teamB)
            teamAWin=prediction.predict(teamA,teamB)
        except:
            errstr="请按照格式填写表单"
            return render(request,'black/game2.html',{'error':errstr})
        s="{}有{}%的概率胜过{}".format(teamA_name,teamAWin,teamB_name)
        return render(request,'black/team_result.html',{'result':s})
    else :
        teamAWin=None
    #print(team_name)
    return render(request,'black/game2.html',{'error':""})
# class ChartTest(APIview):
#     pass

# Create your views here.

def splitString(s):
    i = s.find(':')
    #print("position of ':' ",i)
    name = s[0:i]
    time = s[i+1:len(s)]
    #print("球员 {} :上场时间 {}".format(name,time))
    return [name,time]

'''
2019.6.30
    Database bounded! 
    Following works are: visualizing, formating, advanced searching(date, non-exact name, player link)
'''