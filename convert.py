import base64

with open("icon.ico", "rb") as image:
  str = base64.b64encode(image.read())
  print(str)