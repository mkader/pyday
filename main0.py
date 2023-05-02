import urllib3
import json
import rich

http = urllib3.PoolManager()

response = http.request('GET', 'https://api.zippopotam.us/us/75038')
result = json.loads(response.data.decode('utf-8'))
#print(result)
rich.print(result)

lat = result['places'][0]['latitude']
lng = result['places'][0]['longitude']
rich.print(f'lat:{lat}, lng:{lng}')

response = http.request('GET', f'https://api.sunrisesunset.io/json?lat={lat}&lng={lng}&timezone=CST&date=today')
result = json.loads(response.data.decode('utf-8'))
rich.print(result)

