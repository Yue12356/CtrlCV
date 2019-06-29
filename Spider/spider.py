import bs4
import string 
import asyncio
import time
import aiohttp
import json
from bs4 import BeautifulSoup
import threading
import sys,getopt

player=[]
sem =asyncio.Semaphore(100)
player_stats=['球员','比赛时间','位置','时间','2分命中','2分出手','3分命中','前场','后场','篮板','助攻','犯规','抢断','失误','封盖','得分','正负值','3分出手','罚球命中','罚球出手','2分命中率','3分命中率','罚球命中率','获胜','首发','队名','主客','客队得分','主队得分']
try:
    page_range = (int(sys.argv[1]),int(sys.argv[2]))
except:
    print("请输入参数 <begin num> <end num>")
    sys.exit(-1)
page_num = page_range[1]-page_range[0]
fetch_count = 0
parse_count = 0
#async def fetch(session, url):
#    with(await sem):
#        async with session.get(url) as response:
#            return await response.text()
def split(s):
    i = s.find('-')
    # print(i)
    # print(s[0:i],s[i+1:len(s)])
    score =s[0:i]
    shoot =s[i+1:len(s)]
    return (int(score),int(shoot))


async def parser(url,html):
    try:
        #print("ggg")
        # html = html.decode('utf8')
        #print("decode")
        soup = BeautifulSoup(html, "html.parser")
        timestr = str(soup.find("p",{"class":"time_f"}).string)
    except:
        print(url,"not exist")
        return 
    date = "{}-{}-{}".format(timestr[3:7],timestr[8:10],timestr[11:13])
    #print(timestr,date)
    sit = ""
    team= []
    homeOrAway=["None","0","1"]
    teamIndex=1
    firstZero=1
    awayTotal=str(soup.find("div",{"class":"team_a"})('div')[1]('h2')[0].string).replace("\n","")
    homeTotal=str(soup.find("div",{"class":"team_b"})('div')[1]('h2')[0].string).replace("\n","")
    if(int(awayTotal)>int(homeTotal)):
        awayWin=1
    else:
        awayWin=0
    for tr in soup.find_all("tr"):
        tds=tr('td')
        if tds[0].string=='首发':
            sit="1"
            continue
        if tds[0].string=="替补":
            sit="0"
            continue
        if tds[0].string=="统计":
            #sit="替补"
            continue
        if tds[0].string=="命中率":
            #sit="替补"
            continue
        s={}

        for i in range(len(tds)):
            if i==0 :
                name = str(tds[0].string)
                continue
            try:
                tds[i] = tds[i]('span')[0]
                # print('haha i have a span: ',tds[i].string)
            except:
                pass
            if i==3 and '-' in str(tds[i].string):
                score,shoot = split(str(tds[i].string))
                s['2分命中'] = score
                s['2分出手'] = shoot
                continue
            if i == 4 and '-' in str(tds[i].string):
                score,shoot = split(str(tds[i].string))
                s['3分命中'] = score
                s['3分出手'] = shoot
                s['2分命中'] -= score
                s['2分出手'] -= shoot

                continue
            if i == 5 and '-' in str(tds[i].string):
                score,shoot = split(str(tds[i].string))
                s['罚球命中'] = score
                s['罚球出手'] = shoot
                continue
            # s.append(str(tds[i].string).replace("\n",""))
            s[player_stats[i+1]]=str(tds[i].string).replace("\n","")
            # print("1 ",s)
        if len(s)<11:
            team.append(name)
            continue
        if s['时间']=="0":
            if firstZero==1:
                teamIndex=teamIndex+1
                firstZero=0
            continue
        if s['时间']!="0":
            s[player_stats[-5]]=sit
            s[player_stats[-4]]=team[teamIndex]
            s[player_stats[-3]]=homeOrAway[teamIndex]
            s[player_stats[-2]]=awayTotal
            s[player_stats[-1]]=homeTotal
            # print("2 ",s)
            s['球员']=name
            s['比赛时间']=date
            if s['2分出手'] == 0:
                s['2分命中率'] = 0.0
            else:
                s['2分命中率'] = float(s['2分命中'])/float(s['2分出手'])
            if s['3分出手'] == 0:
                s['3分命中率'] = 0.0
            else:
                s['3分命中率'] = float(s['3分命中'])/float(s['3分出手'])
            if s['罚球出手'] == 0:
                s['罚球命中率'] = 0.0
            else:
                s['罚球命中率'] = float(s['罚球命中'])/float(s['罚球出手'])
            if (teamIndex == 1):
                if(awayWin == 1):
                    s['获胜']=1
                else:
                    s['获胜']=0 
            else:
                if(awayWin == 1):
                    s['获胜']=0
                else:
                    s['获胜']=1
            player.append(s)

async def download(url):
    global fetch_count
    global parse_count
    with(await sem):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                fetch_count+=1
                #html = await fetch(session, url)
                await parser(url,html)
                parse_count+=1

urls=['https://nba.hupu.com/games/boxscore/%d' %i for i in range(page_range[0],page_range[1])]

def print_progress():
    while(1):
        time.sleep(.5)
        global fetch_count
        global parse_count
        fetch_progress = fetch_count/page_num
        parse_progress = parse_count/page_num
        print("Progress: "+">"*int(parse_progress*50)+"="*int((1-parse_progress)*50)+' %.2f'%(parse_progress*100)+"%",flush = True) 
        # print(' %.2f'%(parse_progress*100)+"%",flush = True) 
        if fetch_progress == parse_progress == 1:
            break


print('#'*20)
t1=time.time()
t = threading.Thread(target = print_progress)
t.start()
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(download(url)) for url in urls]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)
with open("result{}_{}.json".format(page_range[0],page_range[1]),"w+",encoding='utf8') as file:
    json.dump(player,file,ensure_ascii=False,indent=0)
t2=time.time()
print("using time :%s"% (t2-t1))
print("#"*20)
print("记录条数：",len(player))