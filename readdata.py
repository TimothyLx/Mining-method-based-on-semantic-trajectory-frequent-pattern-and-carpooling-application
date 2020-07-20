# -*- coding:utf-8 -*-
# @FileName:test.py
# @Time    :2020/7/173:36
# @Author  :LX
import pickle
import time
import xlrd
alist = locals()
a = time.time()
f = xlrd.open_workbook('tag_70591.xlsx',encoding_override='UTF-8')
all_sheet = f.sheets()
n = len(all_sheet)
print(n)
for i in range(n):
    alist['list' + str(i)] = []
for i in range(n):
    for j in range(all_sheet[i].nrows):
     alist['list'+str(i)].append(all_sheet[i].cell(j,1).value)
my_list=[]
for i in range(n):
    my_list.append(alist['list'+str(i)])

with open ('data.pk','wb') as f:
    pickle.dump(my_list,f)

b = time.time()
print(b-a)
# with open('data.pk','rb') as f:
#    b =  pickle.load(f)
# print(b)