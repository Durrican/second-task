import json
import requests
def gethtml(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    html = r.text
    return html

def getProblemlist():
    #获取题目列表
    url = "http://47.102.118.1:8089/api/challenge/list"
    text = json.loads(gethtml(url))
    for t in text:
        print(t)

'''def getproblem():
    url = "http://47.102.118.1:8089/api/challenge/record/d5b3e6e0-9b24-43ca-a6b9-e1094bae5bd2"
    # 每次请求的结果都不一样，动态变化
    text = json.loads(gethtml(url))
    print(text)'''
def getrank():
    #获取队伍排名
    url = "http://47.102.118.1:8089/api/rank"
    text = json.loads(gethtml(url))
    for t in text:
        print(t)

def getundoproblem():
    url = "http://47.102.118.1:8089/api/team/problem/35"
    text = json.loads(gethtml(url))
    for t in text:
        print(t)

def getdoproblem():
    url = "http://47.102.118.1:8089/api/teamdetail/10"
    text = json.loads(gethtml(url))
    for t in text["success"]:
        print(t)

def getDoproblem():
    url = "http://47.102.118.1:8089/api/challenge/record/d33fbc6f-831b-4ecc-9372-982994da1a46"
    text = json.loads(gethtml(url))
    for t in text:
        print(t)

getProblemlist()
getrank()
#getundoproblem()
#getdoproblem()
getDoproblem()