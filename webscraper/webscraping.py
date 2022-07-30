import bs4
import requests
import json
import xlsxwriter,xlrd,sqlite3
from matplotlib import pyplot as plt
url='https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'
header={"content-type": "text/html; charset=UTF-8"}
response=requests.get(url)
soup=bs4.BeautifulSoup(response.content,'html.parser')
country=[]
cases=[]
death=[]
region=[]
row_table=soup.find('table').find_all('tr')[1:]

for col in row_table:
    val=[str(i.text).strip() for i in col]
    print(val)
    country.append(val[1])
    cases.append(val[3])
    death.append(val[5])
    region.append(val[7])
print(country)
print(cases)
print(death)
print(region)

workbook=xlsxwriter.Workbook('corona_virus.xlsx')
worksheet=workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.write('A1','country',bold)
worksheet.write('B1','cases',bold)
worksheet.write('C1','death',bold)
worksheet.write('D1','region',bold)
row=1
col=0

for i in range(len(country)):
    worksheet.write(row, col, country[i])
    worksheet.write(row, col + 1, cases[i])
    worksheet.write(row, col + 2, death[i])
    worksheet.write(row, col + 3, region[i])
    row=row+1

chart1 = workbook.add_chart({'type': 'line'})
chart1.add_series({'categories': '=Sheet1!$B$2:$B$15', 'values': 'Sheet1!$c$2:$c$15'})
chart1.set_title({'name': 'corona_virus'})
worksheet.insert_chart('J4', chart1)

chart2 = workbook.add_chart({'type': 'pie'})
chart2.add_series({'categories': '=Sheet1!$B$2:$B$15', 'values': 'Sheet1!$c$2:$c$15'})
chart2.set_title({'name': 'corona_virus'})
worksheet.insert_chart('J20', chart2)
workbook.close()

wb = xlrd.open_workbook("corona_virus.xlsx")
worksheet = wb.sheet_by_name("Sheet1")
num_rows = worksheet.nrows
num_cols = worksheet.ncols
coln_review=[]

for curr_row in range(0,num_rows, 1):
    row_review = []
    for curr_col in range(0,num_cols,1):
        review = worksheet.cell_value(curr_row, curr_col)
        row_review.append(review)
    coln_review.append(row_review)

conn = sqlite3.connect("corona_virus.db")
print("database connected successfully")
conn.execute('''CREATE TABLE rich( 
    country TEXT NOT NULL, cases TEXT NOT NULL, death TEXT NOT NULL, region TEXT NOT NULL);''')
cursor = conn.cursor()
cursor.executemany('insert into rich (country,cases,death,region) VALUES(?,?,?,?)', coln_review)
conn.commit()
print("operation done successfully")
conn.close()



