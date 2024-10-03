from pandas import *
import pandas as pd
import numpy as np
from openpyxl.workbook import Workbook

# df = pd.DataFrame({'Name': ['Manchester City', 'Real Madrid', 'Liverpool',
#                             'FC Bayern München', 'FC Barcelona', 'Juventus'],
#                    'League': ['English Premier League (1)', 'Spain Primera Division (1)',
#                               'English Premier League (1)', 'German 1. Bundesliga (1)',
#                               'Spain Primera Division (1)', 'Italian Serie A (1)'],
#                    'TransferBudget': [176000000, 188500000, 90000000,
#                                       100000000, 180500000, 105000000]})
#
# df.to_excel('./teams.xlsx', sheet_name='Budgets', index=False)
#
#
# salaries1 = pd.DataFrame({'Name': ['L. Messi', 'Cristiano Ronaldo', 'J. Oblak'],
#                                         'Salary': [560000, 220000, 125000]})
#
# salaries2 = pd.DataFrame({'Name': ['K. De Bruyne', 'Neymar Jr', 'R. Lewandowski'],
#                                         'Salary': [370000, 270000, 240000]})
#
# salaries3 = pd.DataFrame({'Name': ['Alisson', 'M. ter Stegen', 'M. Salah'],
#                                         'Salary': [160000, 260000, 250000]})
#
# salary_sheets = {'Group1': salaries1, 'Group2': salaries2, 'Group3': salaries3}
# writer = pd.ExcelWriter('./salaries.xlsx', engine='xlsxwriter')
#
# for sheet_name in salary_sheets.keys():
#     salary_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
#
# writer._save()

cols = [1, 2, 3, 4]

top_players = pd.read_excel('./stat.xlsx', 'game5', skiprows=[50])
print(top_players.head().columns[4])
