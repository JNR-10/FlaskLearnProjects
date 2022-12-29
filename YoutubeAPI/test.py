import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 12312, "name": "dsacercac", "views": 123412},
        {"likes": 1123112, "name": "sdfvfdvsdf", "views":423412},
        {"likes": 165412, "name": "hfdjgsdf", "views": 127562}]

for i in range(len(data)):
    response = requests.put(BASE + "video/"+str(i),data[i])
    print(response.json())

input() 
response = requests.delete(BASE + "video/0")
print(response)
input()
response = requests.get(BASE + "video/2")
print(response.json())