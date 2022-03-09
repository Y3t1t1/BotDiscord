import json
from types import SimpleNamespace

data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

filename = '.\jeuRP.json'

f = open(filename)

#x = json.loads(f, object_hook=lambda d: SimpleNamespace(**d))

x = json.load(f)

#print(x)

print(x['Tirages'][0]['Tirage'])

for i in x['Tirages']:
    #print(i)
    print('------------------------------')
    #print(i['Cartes'][0]['desc'])
    for j in i['Cartes']:
        print('##########################')
        print(j['desc'])