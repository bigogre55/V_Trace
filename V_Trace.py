#jakes GUI
from tkinter import *
from time import sleep
import socket
import geoIP
import map
import thread
import images
import base64

display = False

def loading():
  try:
    for i in range(0, 23):
      frame = photo2g[i]
      photo.configure(image=frame, background='white')
      photo.image = frame
      main_window.update()
      sleep(45/1000)
  except Exception as e:
    print(e)

def close():
  main_window.destroy()
  exit(0)

def start():
  photo.configure(image=photo2)
  photo.image = photo2
  lbo.delete(0.0, END) 
  lbo.insert(END, "Tracing Route now")
  print('Starting Trace')
  main_window.update()
  trace()

def trace():
  TARGET = lbi.get()
  try:
    geoIP.ipaddress.ip_address(TARGET)
  except:
    print('resolving host')
    try:
      TARGET = socket.gethostbyname(TARGET)
      print("resolved to: " + str(TARGET))
      lbi.delete(0, END)
      lbi.insert(END, TARGET)
      main_window.update()
    except Exception as e:
      print(e)
      lbo.delete(0.0, END)
      photo.configure(image=photo1)
      photo.image = photo1
      lbo.insert(END, "unable to resolve host")
      main_window.update()
      return
  try:
    if 'data' in locals() and display == True:
      print('old data ' + str(data))
    data_thread = thread.TraceThread(TARGET)
    data_thread.daemon = True
    data_thread.start()
    while data_thread.is_alive():
      loading()
    data = data_thread.return_data
    if display == True:
      print('data output')
      print(data)
    out = ""
    u = 0
    for k, v in data[0].items():
      if 'Country' in k:
        out = out + "Country: {}".format(v)
      elif 'State' in k:
        out = out + "State: {}".format(v)
      elif 'City' in k:
        out = out + "City: {}".format(v)
      for i in data[3]:
        if i == k:
          out = out + "Average Latency: {0:.2f}ms".format(data[3][i])
      out = out + '\n'
      u += 1
    lbo.delete(0.0, END)      
  except Exception as e:
    out = "trace failed" + '\n' + str(e)
  if 'data' in locals():
    map.create_route_image(data[1], data[2])
  photo.configure(image=photo1)
  photo.image = photo1
  lbo.insert(END, out)
  lbi.delete(0, END)
  main_window.update()

#Create Images
ifhic = open('icon.ico', 'wb')
ifhic.write(base64.decodebytes(icon_img))
ifhic.close

ifhi = open('image.gif', 'wb')
ifhi.write(base64.b64decode(main_img))
ifhi.close
  
ifhl = open("loading.gif", "wb")
ifhl.write(base64.decodebytes(load_img))
ifhl.close
 
#Define main window
main_window = Tk()
main_window.iconbitmap('icon.ico')
main_window.title(" Jakes Traceroute ")
main_window.configure(background='black')

photo1 = PhotoImage(file='image.gif')
photo2 = PhotoImage(file='loading.gif')
photo2g = [PhotoImage(file='loading.gif', format = 'gif -index %i' %(i)) for i in range(24)]
photo = Label(main_window, image=photo1, bg='black')
photo.grid(column=0, row=0, columnspan=3)

lbi = Entry(main_window, font=('none', 40), width=20)
lbi.grid(column=0, row=1)
lbi.bind("<Return>", (lambda event: start()))

btn = Button(main_window, text='Trace', font=('none', 25), width=5, command=start)
btn.grid(column=0, row=2, sticky=N)

btn_exit = Button(main_window, text='Exit', font=('none', 25), width=5, command=close)
btn_exit.grid(column=0, row=2, sticky=S)

lbo = Text(main_window, height=20, width=40, wrap=WORD, background='white')
lbo.grid(column=2, row=1, sticky=W, rowspan=2)

main_window.mainloop()

#EOF