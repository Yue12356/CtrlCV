import json,os
import aiofiles
import asyncio


async def aload_json():
     print("\n\n\n\n\n\loading file")
     result = ''
     async with aiofiles.open(os.getcwd()+'\\'+'black\\result.json', mode='r', encoding='utf8') as op:
         async for l in op:
             result+=l
     return result

def load_json():
    content=''
    with open(os.getcwd()+'\\'+'black\\result.json','r',encoding='utf8') as op:
        for l in op:
            content+=l

    result=json.loads(content)
    # for i in result:
        # print(i['球员'],' ',i['比赛时间'],' ',i['得分'],' ')
        # print(i,":",result[i])
    return result

if __name__ == '__main__':
    load_json()