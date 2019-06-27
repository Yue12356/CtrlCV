import bs4
import string 
import asyncio
import time
import aiohttp
import json
from bs4 import BeautifulSoup
player={}
sem =asyncio.Semaphore(500)
player_stats=['位置','时间','投篮','3分','罚球','前场','后场','篮板','助攻','犯规','抢断','失误','封盖','得分','+/-','首发','队名','主客','客队得分','主队得分']
#async def fetch(session, url):
#    with(await sem):
#        async with session.get(url) as response:
#            return await response.text()
async def parser(html):
    try:
        #print("ggg")
        # html = html.decode('utf8')
        #print("decode")
        soup = BeautifulSoup(html, "html.parser")
        time = str(soup.find("p",{"class":"time_f"}).string)[3:14]
        sit = ""
        team= []
        homeOrAway=["None","away","home"]
        teamIndex=1
        firstZero=1
        awayTotal=str(soup.find("td",{"class":"item-away-total"}).string).replace("\n","")
        homeTotal=str(soup.find("td",{"class":"item-home-total"}).string).replace("\n","")
        for tr in soup.find_all("tr"):
            tds=tr('td')
            if tds[0].string=='首发':
                sit="首发"
                continue
            if tds[0].string=="替补":
                sit="替补"
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
                # s.append(str(tds[i].string).replace("\n",""))
                s[player_stats[i-1]]=str(tds[i].string).replace("\n","")
                #print("1 ",s)
            if len(s)<9:
                team.append(name)
                continue
            if s[player_stats[1]]=="0":
                if firstZero==1:
                    teamIndex=teamIndex+1
                    firstZero=0
                continue
            if s[player_stats[1]]!="0":
                s[player_stats[-5]]=sit
                s[player_stats[-4]]=team[teamIndex]
                s[player_stats[-3]]=homeOrAway[teamIndex]
                s[player_stats[-2]]=awayTotal
                s[player_stats[-1]]=homeTotal
                #print("2 ",s)
                # s.append(sit)
                # s.append(team[teamIndex])
                # s.append(homeOrAway[teamIndex])
                # s.append(awayTotal)
                # s.append(homeTotal)
                if name not in player:
                    player[name]={}
                player[name][time]=s
                #print(player)
    except:
        pass

async def download(url):
    with(await sem):
        async with aiohttp.ClientSession() as session:
            print("fetch %s" %url)
            async with session.get(url) as response:
                html = await response.text()
                #html = await fetch(session, url)
                print("parser %s" %url)
                await parser(html)

urls=['https://nba.hupu.com/games/boxscore/%d' %i for i in range(156000,157428) ]

def printPlayerList():
    print("Player num:",len(player))
    #print("Game of 凯文-杜兰特：",len(player["凯文-杜兰特"]))
    # for player in ulist:
    #     print(player)
    #     print(ulist[player])

print("#????")
t1=time.time()
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(download(url)) for url in urls]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)
t2=time.time()
print("using time :%s"% (t2-t1))
print("#????")
with open("result.json","w+",encoding='utf8') as file:
    json.dump(player,file,ensure_ascii=False,indent=0)
printPlayerList()
