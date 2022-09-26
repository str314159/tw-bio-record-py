import requests
import json
import datetime
import os

config_open = open("config.json","r")
config_load = json.load(config_open)
list_open = open("list.json", "r+")
list_load = json.load(list_open)

#定数の設定
bearer_token = config_load["token"]["bearer"]
url_before = "https://api.twitter.com/2/users/"
today = str(datetime.datetime.now())
i = 0

if not os.path.isfile("bio_storing_data.json"):
    g = open('bio_storing_data.json','w',encoding='UTF-8')
    g.write({})
    g.close

try:
    json_open = open('bio_storing_data.json','r',encoding='UTF-8')
    data = json.load(json_open)
except:
    flag = input("data reset? Yes or No")
    if flag == "Yes":
        data = {}
    else:
        print("json load error")
        raise ValueError("error!")

#認証用の関数
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r
            
#検索エンドポイントに接続してJSONを取得する関数
def connect_to_endpoint(url, params):
    #APIを叩いて結果を取得
    response = requests.get(url, auth=bearer_oauth, params=params)

    #ステータスコードが200以外ならエラー処理
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    
    return response.json()

def get_user_bio(id):
    url = url_before + id
    params = {'user.fields':'description'}
    response = connect_to_endpoint(url, params)
    return response["data"]["description"]

def get_userId(username):
    url = url_before + "by/username/" + username
    response = connect_to_endpoint(url, {})
    return response["data"]["id"]

for account in list_load["data"]:
    username = account["username"]
    if "id" not in account:
        account.setdefault("id",get_userId(username))
        i += 1
    id = account["id"]
    bio = get_user_bio(id)
    if username in data:
        if bio != data[username][-1]["bio"]:
            data[username].append(
                {
                    'time':today,
                    'bio':bio
                }
            )
    else:
        data.setdefault(username,
        [
            {
                'time':today,
                'bio':bio            
            }
        ])
if i > 0: 
    list_rewrite = open("list.json", "w")
    json.dump(list_load,list_rewrite,indent=4,ensure_ascii=False)

f = open('bio_storing_data.json', 'w', encoding='UTF-8')
json.dump(data,f,indent=4,ensure_ascii=False)
f.close