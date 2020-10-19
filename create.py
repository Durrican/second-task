import json
import requests
def createProblem():
    #创建题目
    url = "http://47.102.118.1:8089/api/challenge/create"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
        'Content-Type': 'application/json'
    }
    data_json = json.dumps({
        "teamid": 35,
    "data": {
        "letter": "a",
        "exclude": 5,
        "challenge": [
            [0, 8, 4],
            [1, 9, 7],
            [2, 6, 3]
        ],
        "step": 19,
        "swap": [1,2]
    },
        "token":"56f315e5-051d-493c-ab96-dc7bb87ea443"
    })
    r = requests.post(url, headers=headers, data=data_json)
    print(r.text)

createProblem()