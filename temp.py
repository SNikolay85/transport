import asyncio
import os
import json
from datetime import date, datetime
from pprint import pprint

# current = os.getcwd()
# file_name = 'datafile.json'
# full_path = os.path.join(current, file_name)
#
# current = os.getcwd()
# file_name = 'driverfile.json'
# f_path = os.path.join(current, file_name)
#
# with open(full_path, 'r', encoding='utf-8') as file:
#     data = json.load(file)
#
# for i in data:
#     if 'pk' in i.keys():
#         del i['pk']
# pprint(data)
# with open(f_path, 'w', encoding='utf-8') as file:
#     json.dump(data, file)

temp_time = datetime.strptime('10%11%22', '%d%%%m%%%y')

first_strdate='10.05.2025'
second_strdate='26-June-2005'
third_strdate='5 Jan, 11'

first_date = datetime.strptime(first_strdate, '%d.%m.%Y')
second_date = datetime.strptime(second_strdate, '%d-%B-%Y')
third_date = datetime.strptime(third_strdate, '%d %b, %y')

print(first_strdate, '->', first_date)
print(second_strdate, '->', second_date)
print(third_strdate, '->', third_date)

print(temp_time)

date_trip = '2024-03-01'
df = datetime.strptime('30-01-12', '%d-%m-%y').date()
print(df)
print(type(df))

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
