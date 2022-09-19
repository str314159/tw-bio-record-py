import json

username = input("username:")

list_open = open("list.json", "r")
list_load = json.load(list_open)
list_load.append({"username":username})
f = open("list.json", "w")
json.dump(list_load,f,indent=4,ensure_ascii=False)
list_open.close
f.close