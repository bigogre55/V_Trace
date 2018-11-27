import gmplot
#import imgkit
import os
import time
import webbrowser

api_key = 'AIzaSyCLBbuwkPn8PZnNiiatbKb6V6M7g01yjy0'
imgkit_options = {
  'javascript-delay': 2000,
}

def fix_html():
  tempHolder=''
  oldLine='<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization&sensor=true_or_false"></script>'
  newLine='<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization&sensor=true_or_false&key={}"></script>'.format(api_key)
  with open('route.html') as fh:
    for line in fh:
      tempHolder += line.replace(oldLine,newLine)
  fh.close

  fh=open('route.html', 'w')
  fh.write(tempHolder)
  fh.close

def map_route(la, lo):
  lal = len(la)
  lol = len(lo)
  map = gmplot.GoogleMapPlotter((sum(la)/float(len(la))), (sum(lo)/float(len(lo))), 5)
  map.scatter(la, lo, size = 50, marker = False)
  map.marker(la[0], lo[0], title="start")
  map.marker(la[-1], lo[-1], title="end")
  map.plot(la, lo, 'blue', edge_width = 2.5)
  map.draw('route.html')

  
def create_image():
  #imgkit.from_file('route.html', 'out.jpg')
  if os.path.exists('route.html'):
    pass
  else:
    time.sleep(2)
  
def create_route_image(la, lo):
  map_route(la, lo)
  fix_html()
  create_image()
  webbrowser.open_new('route.html')
  
if __name__ == '__main__':
  lat = [35.8, 31.3, 31.6]
  long = [58.5, 76.8, 89.4]
  map_route(lat, long)
  if os.path.exists('route.html'):
    create_image()
  else:
    pass