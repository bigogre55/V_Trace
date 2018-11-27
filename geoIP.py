import urllib.request
import urllib.error
import json
import os
import platform
import ipaddress

route = []
display = False
GEO_PATH = {}
lat = []
long = []
PATH = {}


def clear_data():
  global route
  global GEO_PATH
  global PATH
  global lat
  global long
  lat = []
  long = []
  GEO_PATH = {}
  route = []
  PATH = {}
  if display == True:
    print('route' + str(route))
    print('lat' + str(lat))
    print('long' + str(long))
    print('GEO_PATH' + str(GEO_PATH))
    print('PATH' + str(PATH))


def get_info(target, n):
  GEO_DATA = {}
  tla = ""
  tlo = ""
  with urllib.request.urlopen("https://geoip-db.com/jsonp/{}".format(target), timeout=4) as url:
      data = url.read().decode()
      data = data.split("(")[1].strip(")")
      loc_data = json.loads(data)
      if loc_data['state'] == None:
        pass
      else:
        GEO_DATA['hop{}'.format(n)] = n
        GEO_DATA['Country{}'.format(n)] = loc_data['country_name']
        GEO_DATA['City{}'.format(n)] = loc_data['city']
        GEO_DATA['State{}'.format(n)] = loc_data['state']
        GEO_DATA[target] = target
        tla = loc_data['latitude']
        tlo = loc_data['longitude']
        if display == True:
          print(loc_data)
          print(GEO_DATA)
          print(lat)
          print(long)
        lat.append(tla)
        long.append(tlo)
  return GEO_DATA

def OS_trace(HOST):
  if platform.system() == 'Windows':
    HOST_list = os.popen('tracert -d -w 2000 -4 {}'.format(HOST)).read()
  else:
    HOST_list = os.popen('traceroute -n {}'.format(HOST)).read()
  return HOST_list

def validate(HOST_list):
  locations = HOST_list.split(' ')
  for l in locations:
    try:
      if ipaddress.ip_address(l):
        if ipaddress.ip_address(l).is_private:
          pass 
        else:
          route.append(l)
    except ValueError as er:
      pass 
  return route

def get_latency(HOST_list):
  time = {}
  jumble = HOST_list.split('\n')
  for i in jumble:
    tp = i.split(' ')
    ftp = ' '.join(tp).split()
    ftp = [ftp.replace('<1', '0.7') for ftp in ftp]
    try:
      v = ipaddress.ip_address(ftp[-1])
    except:
      if 'v' in locals():
        del v
    if 'v' in locals():
      avg = (float(ftp[1]) + float(ftp[3]) + float(ftp[5]))/3
      time[str(v)] = avg

  return time

def cycle(route):
  n = 0
  for stop in route:
    n+=1
    try:
      PATH.update(get_info(stop, n))
    except urllib.error.URLError as er:
      try:
        PATH.update(get_info(stop, n))
      except urllib.error.URLError as er:
        try:
          PATH.update(get_info(stop, n))
        except urllib.error.URLError as er:
          pass
  return PATH

def main_trace(HOST):
  clear_data()
  HOST_list = OS_trace(HOST)
  latency = get_latency(HOST_list)
  route = validate(HOST_list)

  if route[0] == HOST:
    route.pop(0)

  if display == True:
    print('printing route')
    print("route" + str(route))
  
  tmp = cycle(route) 
  if isinstance(tmp, dict):
    GEO_PATH.update(tmp)
  else:
    pass
  
  data_return = [GEO_PATH, lat, long, latency]
  print('Trace complete')
  return data_return
  
if __name__ == '__main__':
  while True:
    HOST = input("target: ")
    clear_data()
    print(main_trace(HOST))

#EOF