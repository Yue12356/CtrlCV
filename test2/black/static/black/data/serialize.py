import json,os
import copy
import hashlib
import asyncio,aiofiles
def load_json(file_name):
    print('loading ',file_name)
    result = ''
    with open(os.getcwd()+'\\black\\static\\black\\data\\results\\'+file_name,'r',encoding='utf8') as op:
        for l in op:
            result+=l
    return json.loads(result)

def serialize(file_name):
    raw_data = load_json(file_name)
    print('serializing ',file_name)
    name_mapping={
        '位置':'position',
        '时间':'time',
        '2分命中':'two_hit',
        '2分出手':'two_shot',
        '3分命中':'three_hit',
        '3分出手':'three_shot',
        '罚球命中':'penalty_hit',
        '罚球出手':'penalty_shot',
        '前场':'front',
        '后场':'back',
        '篮板':'bord',
        '助攻':'sup',
        '犯规':'foul',
        '抢断':'ST',
        '失误':'miss',
        '封盖':'block',
        '得分':'point',
        '正负值':'ZF',
        '首发':'first',
        '队名':'team_name',
        '主客':'HA',
        '客队得分':'A_point',
        '主队得分':'H_point',
        '球员':'player_name',
        '比赛时间':'game_time',
        '2分命中率':'two_rate',
        '3分命中率':'three_rate',
        '罚球命中率':'penalty_rate',
        '获胜':'wining'        
    }
    serialized  =[]
    m=hashlib.md5()
    for d in raw_data:
        m.update((d['球员']+d['比赛时间']).encode('utf8'))
        temp = {'pk':m.hexdigest(),'model':'black.PlayerInfo','fields':{}}
        # temp['pk'=]
        for k in d:
            if k == '比赛时间':
                d[k] = d[k].replace('年','-').replace('月','-')[:-1]
            if d[k] == 'None':
                d[k] = 0
            temp['fields'][name_mapping[k]]=d[k]
        flag = 0
        for k in temp['fields']:
            if temp['fields'][k]=='None' or temp['fields'][k]=='NA':
                flag = 1
        if flag ==1:
            continue
        serialized.append(copy.deepcopy(temp))
    with open('black\\fixtures\\serialized_'+file_name,"w+",encoding='utf8') as file:
        json.dump(serialized,file,ensure_ascii=False,indent=0)
    return serialized
    pass

[
    {
        "pk": "4b678b301dfd8a4e0dad910de3ae245b",
        "model": "sessions.session",
        "fields": {
            "expire_date": "2013-01-16T08:16:59.844Z",
        }
    }
]

if __name__ =='__main__':
    # print(load_json())
    # print(serialize())
    files = []
    for f in os.walk(os.getcwd()+'\\black\\static\\black\\data\\results'):
        files = f[2]
    for name in files[:1]:
        print(name)
        serialize(name)