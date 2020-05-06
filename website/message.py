from smsc_api import *

smsc = SMSC()
r = smsc.send_sms("79241701065", "Напиши что нибудь угарное", format=0, translit=1)
print(r)