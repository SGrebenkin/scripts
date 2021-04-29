import requests
import json
import os.path
from math import cos, asin, sqrt, pi

def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a))

TOKEN="yourtokenfrom ads-api.ru" # You need to get the token from ads-api.ru
USER="username@gmail.com" # Your email


#if not os.path.isfile("data.txt"):
if True:
    r = requests.get('https://ads-api.ru/main/api', params={'user':USER,'token':TOKEN,'category_id':2,'source':1,'city':'Краснодарский край, Сочи','is_actual':1,'date1':'2021-04-19 00:00:00','param[1943]':'Сдам','param[2016]':'На длительный срок'})
    print(r.status_code)
    with open("data.txt", "w") as json_file:
        json.dump(r.text, json_file)

object = {}
with open("data.txt", "r") as json_file:
    object = json.load(json_file)

object = json.loads(object)

results = {}
for i in object["data"]:
    if int(i['price']) > 45000:
        continue

    center_lat = 43.583547
    center_lon = 39.720578
    lat = float(i['coords']['lat'])
    lon = float(i['coords']['lng'])
    dist = distance(center_lat, center_lon, lat, lon)
    if dist > 10:
        continue

    if not int(i['price']) in results.keys():
        results[int(i['price'])] = []
    results[int(i['price'])].append(i['url'] + "\t" + i['time'] + "\t" + str(round(dist,2)) + "km \t" + str(i))

for i in sorted (results.keys()):
    for j in results[i]:
        print(str(i) + " rub \t" + str(j))

