#!/usr/bin/python3

import tkinter as tk
from datetime import datetime
from datetime import timedelta
import sys
import os


# row 0:  lab1 - time
# row 1:  top button
# row 2:  
# row 3:
# row 4:  lab2 - Click when...
# row 5:  lab3 - timer (count-down)
# row 6:  
# row 7:  mes4  - sava specs
# row 8:  2nd button



############################################
fname_conf_default = 'default/savitime.config'
fname_conf_user = 'user/savitime.config'

f = open(fname_conf_default)
for l in f:
  for l in f:
    if not l.startswith('!'):  continue
    l = l.strip()
    ll = l.split(' ')
    key = ll[0]
    ###
    if key == '!sava_fps':  sava_fps = int(ll[1])
    elif key == '!sava_n_frames':  sava_n_frames = int(ll[1])
    elif key == '!wait_max':  wait_max = int(ll[1])
    elif key == '!stabilization_delay':
      stabilization_delay = int(ll[1])
    else:
      print("Error.  Unrecognized key.")
      print("  key: ", key)
      sys.exit(1)
f.close()
############################################
if os.path.exists(fname_conf_user):
 f = open(fname_conf_user)
 for l in f:
   for l in f:
     if not l.startswith('!'):  continue
     l = l.strip()
     ll = l.split(' ')
     key = ll[0]
     ###
     if key == '!sava_fps':  sava_fps = int(ll[1])
     elif key == '!sava_n_frames':  sava_n_frames = int(ll[1])
     elif key == '!wait_max':  wait_max = int(ll[1])
     elif key == '!stabilization_delay':
       stabilization_delay = int(ll[1])
     else:
       print("Error.  Unrecognized key.")
       print("  key: ", key)
       sys.exit(1)
 f.close()
############################################

# sava_fps = 120.0
# sava_n_frames = 512
sava_vid_len = sava_n_frames / sava_fps  # in seconds

# font1 = ("Arial Bold", 30)
font1 = ("Monospace", 14)
font2 = ("Monospace Bold", 12)
font4 = ("Monospace", 10)





##################################################################
class c_savitime:
  def __init__(self):
    self.clickmode = 0
    self.dt1 = int((stabilization_delay+sava_vid_len) * 1000)
    self.dt2 = wait_max * 1000
  ###
  def run(self):
    #
    self.clickmode = 0
    self.unow = datetime.now()
    #
    self.root = tk.Tk()
    self.root.geometry('300x600')
    self.root.title("SAVA video timer.")
    #
    self.lab1 = tk.Label(text="", font=font2, fg="#009999")
    self.lab1.grid(column=0, row=0, sticky=tk.W)
    #
    self.lab2 = tk.Label(text="Click when focus is done.", font=font1, fg="#000000")
    self.lab2.grid(column=0, row=4)
    #
    self.lab3 = tk.Label(text="", font=font1, fg="#009999")
    self.lab3.grid(column=0, row=5, sticky=tk.W)
    #
    #
    text4 = "\n"
    text4 += "sava fps:  {0:0.0f}\n".format(sava_fps)
    text4 += "sava frames: {0:0.0f}\n".format(sava_n_frames)
    text4 += "sava vid len: {0:0.1f}s\n".format(sava_vid_len)
    text4 += "wait time: {0:0.1f}s".format( self.dt1/1000 )
    self.mes4 = tk.Message(text=text4, font=font4, fg="#000000", width=240)
    self.mes4.grid(column=0, row=7, sticky=tk.W)
    #
    self.btn1 = tk.Button(self.root, text="Ready.",
      bg="#222288", fg="#ffff00",
      width=30, height=10,
      command=self.click1
      )
    self.btn1.grid(column=0, row=2, sticky=tk.W)
    #
    self.btn2 = tk.Button(self.root, text="---",
      bg="#777788", fg="#ffff88",
      width=30, height=3,
      command=self.click2
      )
    self.btn2.grid(column=0, row=8, sticky=tk.W)
    #
    self.timer_t0_dto = datetime.now()
    self.timer_dt = 0
    self.timermode = 0
    #
    self.run1()
  ###
  def run1(self):
    self.run_clock()
    self.root.mainloop()
  ###
  def run_clock(self):
    self.unow = datetime.now()
    now = self.unow.strftime("%H:%M:%S")
    self.lab1.configure(text=now)
    self.root.after(100, self.run_clock)
    self.run_timer()
  ###
  def run_timer(self):
    if self.timermode == 0:
      self.lab3.configure(text="---")
    else:
      dt = self.timer_dt - (self.unow - self.timer_t0_dto).total_seconds()
      self.lab3.configure(text="{0:0.1f}s".format(dt))
      self.root.after(100, self.run_timer)
    if self.timermode == 1 and dt <= 0:
      self.timermode = 2
      self.lab2.configure(text="Ready to save.")
      self.btn1.configure(
        bg="#228822", fg="#ffff00",
        )
      self.timer_t0_dto = datetime.now()
      self.timer_dt = self.dt2/1000
    elif self.timermode == 2 and dt <= 0:
      self.lab2.configure(text="Time is up - save now.")
      self.btn1.configure(
        bg="#882222", fg="#ffff00",
        )
      self.clickmode = 2
      self.timemode = 3
  ###
  def click1(self):
    if 1:
      self.clickmode = 1
      self.timer_t0_dto = datetime.now()
      self.timer_dt = self.dt1/1000
      self.timermode = 1
      self.lab2.configure(text="Waiting...")
      self.btn1.configure(text="Restart",
          bg="#777788", fg="#ffff88"
        )
      self.btn2.configure(text="Cancel")
  ###
  def click2(self):
    if self.clickmode > 0:
      self.clickmode = 0
      self.timermode = 0
      self.btn1.configure(text="Ready.",
        bg="#222288", fg="#ffff00"
        )
      self.lab2.configure(text="Click when focus is done.")
      self.btn2.configure(text="---")
  ###
  ###
  ###
##################################################################

savitime = c_savitime()



