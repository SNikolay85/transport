import asyncio
import os
import json
from pprint import pprint

current = os.getcwd()
file_name = 'datafile.json'
full_path = os.path.join(current, file_name)

current = os.getcwd()
file_name = 'driverfile.json'
f_path = os.path.join(current, file_name)

with open(full_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

for i in data:
    if 'pk' in i.keys():
        del i['pk']
pprint(data)
with open(f_path, 'w', encoding='utf-8') as file:
    json.dump(data, file)

async def foo():
    return 42

async def ggg():
    df_1 = foo()
    df_2 = foo()
    res = await asyncio.gather(df_1, df_2)
    return res


if __name__ == '__main__':
    print(asyncio.run(ggg()))
    #print(asyncio.run(ggg()))
