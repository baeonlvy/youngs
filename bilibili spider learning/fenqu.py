from pandas.core.construction import array
from requests import get

import json

import csv

import pandas as pd 

from pandas import DataFrame

import numpy as count

import matplotlib.pyplot as plt

origin_url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid={}&type=all"
#查找每一个分类的rid
part_rid = {
    "cartoon": 1, 
    "music": 3, 
    "dance": 129, 
    "game": 4, 
    "knowledge": 36, 
    "technology": 188, 
    "sport": 234, 
    "car": 223, 
    "life": 160, 
    "food": 211, 
    "animal": 217, 
    "memes": 119, 
    "fashion": 155, 
    "entertainment": 5, 
    "movie": 181
}
#将每一个分类的所有热门视频的播放量和点赞数
for key in part_rid.keys():
    with open("part_data/{}.csv".format(key), "w" , encoding="utf-8") as csv_file:
        csv_stringlist=[]
        csv_stringlist.append("title,view_num,likes\n")
        rasp = get(origin_url.format(part_rid[key]))
        video_list = json.loads(rasp.text)["data"]["list"]
        for video in video_list:
           csv_stringlist.append("\"{}\", {}, {},\n".format(video["title"], video["stat"]["view"],video["stat"]["like"]))
        csv_file.writelines(csv_stringlist)
#创建一个结构体
"""class bilicount:
   def __init__(self,name,num,like):
       self.name=name
       self.num=num
       self.like=like
"""
#创建写入excel的方法
writer1= pd.ExcelWriter("excel_part/viewnum.xlsx")
writer2= pd.ExcelWriter("excel_part/likenum.xlsx")
#读取csv文件的内容
nameall=[]
percentlike=[]
alldataviewnum=[]
alldatalikenum=[]
for key in part_rid.keys():
     with open("part_data/{}.csv".format(key), "r", encoding="utf-8") as csv_file:
         csv_reader=csv.reader(csv_file)
         nameall.append(str(key))
         datavw =[]
         datalk =[]
         datacol1 = []
         datacol2 = [] 
         for row in csv_reader:
             datavw.append(row[1])
             datalk.append(row[2])
         del datavw[0],datalk[0]
         for i in range(len(datalk)):
             datacol2.append(int(datalk[i]))
         for i in range(len(datavw)):
             datacol1.append(int(datavw[i]))
         allviewnum=sum(datacol1)
         alldataviewnum.append(allviewnum)
         alllikenum=sum(datacol2)
         alldatalikenum.append(alllikenum)
         print("{}类视频的观看量为；{} , 点赞数为: {}".format(key,allviewnum,alllikenum))
         evregeviewnum=float(allviewnum)/100
         evregelikenum=float(alllikenum)/100
         print("平均播放量为:{},平均点赞数为:{}".format(evregeviewnum,evregelikenum)) 
         percentlike.append(alllikenum/allviewnum)
print(nameall)
print(alldataviewnum)
print(alldatalikenum)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(1)
plt.bar(nameall,alldataviewnum)
plt.xlabel("分区")
plt.ylabel("热门视频总播放量")
plt.title("不同分区播放量对比")
plt.show()
fig=plt.figure(2)
plt.bar(nameall,alldatalikenum)
plt.xlabel("分区")
plt.ylabel("热门视频总点赞量")
plt.title("不同分区点赞量对比")
plt.show()
fig=plt.figure(3)
plt.bar(nameall,percentlike)
plt.xlabel("分区")
plt.ylabel("热门视频点赞播放比率")
plt.title("不同分区观看者是否愿意点赞")
plt.show()
data1={'分区':nameall,'总播放量':alldataviewnum}
data2={'分区':nameall,'总点赞量':alldatalikenum}
data3={'分区':nameall,'点赞比率':percentlike}
df=DataFrame(data1)
df.to_excel('excel_part/viewnum.xlsx',index=False)
df=DataFrame(data2)
df.to_excel('excel_part/likenum.xlsx',index=False)
df=DataFrame(data3)
df.to_excel('excel_part/percentlike.xlsx',index=False)