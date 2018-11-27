#dep file for traceroute
import pip

def fix_dep():
  try:
    import gmplot
  except:
    print('missing gmplot')
    pip.main(['install', gmplot])

#  try:
#    import imgkit
#  except:
#    print('missing imgkit')
#    pip.main(['install', imgkit])

  try:
    import tkinter
  except:
    print('missing tkinter')
    pip.main(['install', tkinter])