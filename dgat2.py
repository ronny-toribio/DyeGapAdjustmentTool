#!/usr/bin/python3
# Author: Ronny Toribio
# Project: Dye Gap Adjustment Tool
# Description: A dye gap adjustment tool that uses an XML REST API and apa_data.xml.
import os
import os.path
from time import sleep
from xml.dom.minidom import parseString as parseXMLString

import_errors = 0
try:
   import tkinter as tk
   import tkinter.ttk as ttk
   from tkinter import filedialog
   from tkinter import messagebox
except:
   print("The tkinter module is not installed.")
   import_errors += 1
try:
   from requests import post, get
except:
   print("The requests module is not installed.")
   import_errors += 1
if import_errors:
   exit(1)

DEFAULT_STATUS = " Reading current dye values."
FILE_LOAD_SUCCESSFULL = " The apa_data.xml file was loaded successfully."
FILE_SAVE_SUCCESSFULL = " The changes were saved successfully."
FILE_SAVE_UNSUCCESSFULL = "The changes could not be saved."
UNSAVED_CHANGES = " There are unsaved changes."
PRINTER_IP = "127.0.0.1"
RAW_SET_DYE_COMMAND = """<?xml version="1.0" encoding="UTF-8"?>
<ompcap:OemsiMediapathFunc xmlns:ompcap=http://www.hp.com/schemas/imaging/con/ledm/oemsimediapathcap/2008/03/21 \>
   <ompcap:CmdCode>0x12</ompcap:CmdCode>
   <ompcap:InputParam type="string">oem_set_alignment_values 0 0 {} {} {} {}</ompcap:InputParam>
</ompcap:OemsiMediapathFunc>"""

GAP_VALUE_RANGE = [-200, -192, -184, -176, -168, -160, -152, -144, -136, -128, -120, -112, -104, -96, -88, -80, -72, -64, -56, -48, -40, -32, -24, -16, -8, 0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200]

def last_print_value(dye):
   if dye == 0:
      return 1200
   else:
      return 19200

def set_dye(dye, color, value):
   r = post("http://{}/OemsiMediapath/Function".format(PRINTER_IP), data=RAW_SET_DYE_COMMAND.format(dye, color, value, last_print_value(dye)))
   if r.status_code != 200:
      messagebox.showinfo("set_dye() error", "HTTP response code is {}".format(r.status_code))
      return False
   return True

def check_status():
   r = get("http://{}/OemsiMediapath/Function".format(PRINTER_IP))
   if r.status_code != 200:
      messagebox.showinfo("check_status() error", "HTTP response code is {}".format(r.status_code))
      return False
   content = r.content
   if content:
      if content[0] == "0":
         return True
      else:
         messagebox.showinfo("check_status() error", "Content is {}".format(content))
   return False

class DyeGapAdjustmentTool:
   filepath = None
   has_changed = False
   def __init__(self):
      self.root = tk.Tk()
      width = 418
      height = 355
      screen_wcenter = int((self.root.winfo_screenwidth() / 2) - (width / 2))
      screen_hcenter = int((self.root.winfo_screenheight() / 2) - (height / 2))
      self.root.geometry("{}x{}+{}+{}".format(width, height, screen_wcenter, screen_hcenter))
      self.root.resizable(False, False)
      self.root.title("Dye Gap Adjustment Tool")

      # Keyboard Shortcuts
      self.root.bind("<Control-o>", lambda e: self.load_APA_file())
      self.root.bind("<Control-l>", lambda e: self.load_APA_file())
      self.root.bind("<Control-s>", lambda e: self.save_changes())
      self.root.bind("<Control-q>", lambda e: self.root.quit())

      # Menu Bar
      self.menubar = tk.Menu(self.root)
      self.filemenu = tk.Menu(self.menubar, tearoff=0)
      self.filemenu.add_command(label="Open", command=self.load_APA_file, accelerator="Ctrl+O")
      self.filemenu.add_command(label="Save", command=self.save_changes, accelerator="Ctrl+S")
      self.filemenu.add_separator()
      self.filemenu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
      self.menubar.add_cascade(label="File", menu=self.filemenu)
      self.helpmenu = tk.Menu(self.menubar, tearoff=0)
      self.helpmenu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Dye Gap Adjustment Tool\nDeveloped by Ronny Toribio."))
      self.menubar.add_cascade(label="Help", menu=self.helpmenu)
      self.root.config(menu=self.menubar)

      # Main Panels
      self.dyes_panel = tk.Frame(self.root)
      self.dyes_panel.pack()
      self.button_panel = tk.Frame(self.root)
      self.button_panel.pack(padx=20, pady=20)
      self.status_panel = tk.Frame(self.root)
      self.status_panel.pack(side=tk.BOTTOM, fill=tk.X)

      # Status Bar
      self.statusVar = tk.StringVar()
      self.statusBar = tk.Label(self.status_panel, textvariable=self.statusVar, bd=1, width=59, relief=tk.SUNKEN, anchor=tk.W, font=("arial", 10, "normal"))
      self.statusBar.pack()
      self.statusVar.set(DEFAULT_STATUS)

      # Dye 0
      self.dye_0_var = tk.IntVar()
      self.dye_0_var.set(0)
      self.dye_0_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 0")
      self.dye_0_panel.grid(column=0, row=0, padx=5, pady=5)
      self.dye_0_lab = tk.Label(self.dye_0_panel, width=4, textvariable=self.dye_0_var)
      self.dye_0_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_0_inc = tk.Button(self.dye_0_panel, text="U", command=self.increment_dye_0)
      self.dye_0_inc.grid(column=1, row=0)
      self.dye_0_inc["state"] = "disable"
      self.dye_0_dec = tk.Button(self.dye_0_panel, text="D", command=self.decrement_dye_0)
      self.dye_0_dec.grid(column=1, row=1)
      self.dye_0_dec["state"] = "disable"

      # Dye 1
      self.dye_1_var = tk.IntVar()
      self.dye_1_var.set(0)
      self.dye_1_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 1")
      self.dye_1_panel.grid(column=1, row=0, padx=5, pady=5)
      self.dye_1_lab = tk.Label(self.dye_1_panel, width=4, textvariable=self.dye_1_var)
      self.dye_1_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_1_inc = tk.Button(self.dye_1_panel, text="U", command=self.increment_dye_1)
      self.dye_1_inc.grid(column=1, row=0)
      self.dye_1_inc["state"] = "disable"
      self.dye_1_dec = tk.Button(self.dye_1_panel, text="D", command=self.decrement_dye_1)
      self.dye_1_dec.grid(column=1, row=1)
      self.dye_1_dec["state"] = "disable"

      # Dye 2
      self.dye_2_var = tk.IntVar()
      self.dye_2_var.set(0)
      self.dye_2_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 2")
      self.dye_2_panel.grid(column=2, row=0, padx=5, pady=5)
      self.dye_2_lab = tk.Label(self.dye_2_panel, width=4, textvariable=self.dye_2_var)
      self.dye_2_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_2_inc = tk.Button(self.dye_2_panel, text="U", command=self.increment_dye_2)
      self.dye_2_inc.grid(column=1, row=0)
      self.dye_2_inc["state"] = "disable"
      self.dye_2_dec = tk.Button(self.dye_2_panel, text="D", command=self.decrement_dye_2)
      self.dye_2_dec.grid(column=1, row=1)
      self.dye_2_dec["state"] = "disable"

      # Dye 3
      self.dye_3_var = tk.IntVar()
      self.dye_3_var.set(0)
      self.dye_3_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 3")
      self.dye_3_panel.grid(column=3, row=0, padx=5, pady=5)
      self.dye_3_lab = tk.Label(self.dye_3_panel, width=4, textvariable=self.dye_3_var)
      self.dye_3_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_3_inc = tk.Button(self.dye_3_panel, text="U", command=self.increment_dye_3)
      self.dye_3_inc.grid(column=1, row=0)
      self.dye_3_inc["state"] = "disable"
      self.dye_3_dec = tk.Button(self.dye_3_panel, text="D", command=self.decrement_dye_3)
      self.dye_3_dec.grid(column=1, row=1)
      self.dye_3_dec["state"] = "disable"

      # Dye 4
      self.dye_4_var = tk.IntVar()
      self.dye_4_var.set(0)
      self.dye_4_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 4")
      self.dye_4_panel.grid(column=4, row=0, padx=5, pady=5)
      self.dye_4_panel.grid_propagate(1)
      self.dye_4_lab = tk.Label(self.dye_4_panel, width=4, textvariable=self.dye_4_var)
      self.dye_4_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_4_inc = tk.Button(self.dye_4_panel, text="U", command=self.increment_dye_4)
      self.dye_4_inc.grid(column=1, row=0)
      self.dye_4_inc["state"] = "disable"
      self.dye_4_dec = tk.Button(self.dye_4_panel, text="D", command=self.decrement_dye_4)
      self.dye_4_dec.grid(column=1, row=1)
      self.dye_4_dec["state"] = "disable"

      # Dye 5
      self.dye_5_var = tk.IntVar()
      self.dye_5_var.set(0)
      self.dye_5_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 5")
      self.dye_5_panel.grid(column=0, row=1, padx=5, pady=5)
      self.dye_5_lab = tk.Label(self.dye_5_panel, width=4, textvariable=self.dye_5_var)
      self.dye_5_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_5_inc = tk.Button(self.dye_5_panel, text="U", command=self.increment_dye_5)
      self.dye_5_inc.grid(column=1, row=0)
      self.dye_5_inc["state"] = "disable"
      self.dye_5_dec = tk.Button(self.dye_5_panel, text="D", command=self.decrement_dye_5)
      self.dye_5_dec.grid(column=1, row=1)
      self.dye_5_dec["state"] = "disable"

      # Dye 6
      self.dye_6_var = tk.IntVar()
      self.dye_6_var.set(0)
      self.dye_6_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 6")
      self.dye_6_panel.grid(column=1, row=1, padx=5, pady=5)
      self.dye_6_lab = tk.Label(self.dye_6_panel, width=4, textvariable=self.dye_6_var)
      self.dye_6_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_6_inc = tk.Button(self.dye_6_panel, text="U", command=self.increment_dye_6)
      self.dye_6_inc.grid(column=1, row=0)
      self.dye_6_inc["state"] = "disable"
      self.dye_6_dec = tk.Button(self.dye_6_panel, text="D", command=self.decrement_dye_6)
      self.dye_6_dec.grid(column=1, row=1)
      self.dye_6_dec["state"] = "disable"

      # Dye 7
      self.dye_7_var = tk.IntVar()
      self.dye_7_var.set(0)
      self.dye_7_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 7")
      self.dye_7_panel.grid(column=2, row=1, padx=5, pady=5)
      self.dye_7_lab = tk.Label(self.dye_7_panel, width=4, textvariable=self.dye_7_var)
      self.dye_7_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_7_inc = tk.Button(self.dye_7_panel, text="U", command=self.increment_dye_7)
      self.dye_7_inc.grid(column=1, row=0)
      self.dye_7_inc["state"] = "disable"
      self.dye_7_dec = tk.Button(self.dye_7_panel, text="D", command=self.decrement_dye_7)
      self.dye_7_dec.grid(column=1, row=1)
      self.dye_7_dec["state"] = "disable"

      # Dye 8
      self.dye_8_var = tk.IntVar()
      self.dye_8_var.set(0)
      self.dye_8_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 8")
      self.dye_8_panel.grid(column=3, row=1, padx=5, pady=5)
      self.dye_8_lab = tk.Label(self.dye_8_panel, width=4, textvariable=self.dye_8_var)
      self.dye_8_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_8_inc = tk.Button(self.dye_8_panel, text="U", command=self.increment_dye_8)
      self.dye_8_inc.grid(column=1, row=0)
      self.dye_8_inc["state"] = "disable"
      self.dye_8_dec = tk.Button(self.dye_8_panel, text="D", command=self.decrement_dye_8)
      self.dye_8_dec.grid(column=1, row=1)
      self.dye_8_dec["state"] = "disable"

      # Dye 9
      self.dye_9_var = tk.IntVar()
      self.dye_9_var.set(0)
      self.dye_9_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 9")
      self.dye_9_panel.grid(column=4, row=1, padx=5, pady=5)
      self.dye_9_lab = tk.Label(self.dye_9_panel, width=4, textvariable=self.dye_9_var)
      self.dye_9_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_9_inc = tk.Button(self.dye_9_panel, text="U", command=self.increment_dye_9)
      self.dye_9_inc.grid(column=1, row=0)
      self.dye_9_inc["state"] = "disable"
      self.dye_9_dec = tk.Button(self.dye_9_panel, text="D", command=self.decrement_dye_9)
      self.dye_9_dec.grid(column=1, row=1)
      self.dye_9_dec["state"] = "disable"

      # Dye 10
      self.dye_10_var = tk.IntVar()
      self.dye_10_var.set(0)
      self.dye_10_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 10")
      self.dye_10_panel.grid(column=0, row=2, padx=5, pady=5)
      self.dye_10_lab = tk.Label(self.dye_10_panel, width=4, textvariable=self.dye_10_var)
      self.dye_10_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_10_inc = tk.Button(self.dye_10_panel, text="U", command=self.increment_dye_10)
      self.dye_10_inc.grid(column=1, row=0)
      self.dye_10_inc["state"] = "disable"
      self.dye_10_dec = tk.Button(self.dye_10_panel, text="D", command=self.decrement_dye_10)
      self.dye_10_dec.grid(column=1, row=1)
      self.dye_10_dec["state"] = "disable"

      # Dye 11
      self.dye_11_var = tk.IntVar()
      self.dye_11_var.set(0)
      self.dye_11_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 11")
      self.dye_11_panel.grid(column=1, row=2, padx=5, pady=5)
      self.dye_11_lab = tk.Label(self.dye_11_panel, width=4, textvariable=self.dye_11_var)
      self.dye_11_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_11_inc = tk.Button(self.dye_11_panel, text="U", command=self.increment_dye_11)
      self.dye_11_inc.grid(column=1, row=0)
      self.dye_11_inc["state"] = "disable"
      self.dye_11_dec = tk.Button(self.dye_11_panel, text="D", command=self.decrement_dye_11)
      self.dye_11_dec.grid(column=1, row=1)
      self.dye_11_dec["state"] = "disable"

      # Dye 12
      self.dye_12_var = tk.IntVar()
      self.dye_12_var.set(0)
      self.dye_12_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 12")
      self.dye_12_panel.grid(column=2, row=2, padx=5, pady=5)
      self.dye_12_lab = tk.Label(self.dye_12_panel, width=4, textvariable=self.dye_12_var)
      self.dye_12_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_12_inc = tk.Button(self.dye_12_panel, text="U", command=self.increment_dye_12)
      self.dye_12_inc.grid(column=1, row=0)
      self.dye_12_inc["state"] = "disable"
      self.dye_12_dec = tk.Button(self.dye_12_panel, text="D", command=self.decrement_dye_12)
      self.dye_12_dec.grid(column=1, row=1)
      self.dye_12_dec["state"] = "disable"

      # Dye 13
      self.dye_13_var = tk.IntVar()
      self.dye_13_var.set(0)
      self.dye_13_panel = ttk.LabelFrame(self.dyes_panel, text="Dye 13")
      self.dye_13_panel.grid(column=3, row=2, padx=5, pady=5)
      self.dye_13_lab = tk.Label(self.dye_13_panel, width=4, textvariable=self.dye_13_var)
      self.dye_13_lab.grid(column=0, row=0, ipadx=2, ipady=2)
      self.dye_13_inc = tk.Button(self.dye_13_panel, text="U", command=self.increment_dye_13)
      self.dye_13_inc.grid(column=1, row=0)
      self.dye_13_inc["state"] = "disable"
      self.dye_13_dec = tk.Button(self.dye_13_panel, text="D", command=self.decrement_dye_13)
      self.dye_13_dec.grid(column=1, row=1)
      self.dye_13_dec["state"] = "disable"

      # Dye Variables List
      self.dye_vars = [self.dye_0_var,
                       self.dye_1_var,
                       self.dye_2_var,
                       self.dye_3_var,
                       self.dye_4_var,
                       self.dye_5_var,
                       self.dye_6_var,
                       self.dye_7_var,
                       self.dye_8_var,
                       self.dye_9_var,
                       self.dye_10_var,
                       self.dye_11_var,
                       self.dye_12_var,
                       self.dye_13_var]

      # Changed Dyes Set
      self.changed_dyes = set()

      # Operation Buttons
      self.load_button = tk.Button(self.button_panel, text="Load File", command=self.load_APA_file)
      self.load_button.grid(column=0, row=6)
      self.save_button = tk.Button(self.button_panel, text="Apply Changes", command=self.save_changes)
      self.save_button.grid(column=1, row=6)
      self.save_button["state"] = "disabled"

      # Increase/Decrease Button Images
      if os.path.exists("tri-up.png") and os.path.exists("tri-down.png"):
         tri_up = tk.PhotoImage(file="tri-up.png")
         tri_down = tk.PhotoImage(file="tri-down.png")
         self.dye_0_inc.configure(image=tri_up, text="")
         self.dye_0_dec.configure(image=tri_down, text="")
         self.dye_0_inc.image = tri_up
         self.dye_0_dec.image = tri_down
         self.dye_1_inc.configure(image=tri_up, text="")
         self.dye_1_dec.configure(image=tri_down, text="")
         self.dye_1_inc.image = tri_up
         self.dye_1_dec.image = tri_down
         self.dye_2_inc.configure(image=tri_up, text="")
         self.dye_2_dec.configure(image=tri_down, text="")
         self.dye_2_inc.image = tri_up
         self.dye_2_dec.image = tri_down
         self.dye_3_inc.configure(image=tri_up, text="")
         self.dye_3_dec.configure(image=tri_down, text="")
         self.dye_3_inc.image = tri_up
         self.dye_3_dec.image = tri_down
         self.dye_4_inc.configure(image=tri_up, text="")
         self.dye_4_dec.configure(image=tri_down, text="")
         self.dye_4_inc.image = tri_up
         self.dye_4_dec.image = tri_down
         self.dye_5_inc.configure(image=tri_up, text="")
         self.dye_5_dec.configure(image=tri_down, text="")
         self.dye_5_inc.image = tri_up
         self.dye_5_dec.image = tri_down
         self.dye_6_inc.configure(image=tri_up, text="")
         self.dye_6_dec.configure(image=tri_down, text="")
         self.dye_6_inc.image = tri_up
         self.dye_6_dec.image = tri_down
         self.dye_7_inc.configure(image=tri_up, text="")
         self.dye_7_dec.configure(image=tri_down, text="")
         self.dye_7_inc.image = tri_up
         self.dye_7_dec.image = tri_down
         self.dye_8_inc.configure(image=tri_up, text="")
         self.dye_8_dec.configure(image=tri_down, text="")
         self.dye_8_inc.image = tri_up
         self.dye_8_dec.image = tri_down
         self.dye_9_inc.configure(image=tri_up, text="")
         self.dye_9_dec.configure(image=tri_down, text="")
         self.dye_9_inc.image = tri_up
         self.dye_9_dec.image = tri_down
         self.dye_10_inc.configure(image=tri_up, text="")
         self.dye_10_dec.configure(image=tri_down, text="")
         self.dye_10_inc.image = tri_up
         self.dye_10_dec.image = tri_down
         self.dye_11_inc.configure(image=tri_up, text="")
         self.dye_11_dec.configure(image=tri_down, text="")
         self.dye_11_inc.image = tri_up
         self.dye_11_dec.image = tri_down
         self.dye_12_inc.configure(image=tri_up, text="")
         self.dye_12_dec.configure(image=tri_down, text="")
         self.dye_12_inc.image = tri_up
         self.dye_12_dec.image = tri_down
         self.dye_13_inc.configure(image=tri_up, text="")
         self.dye_13_dec.configure(image=tri_down, text="")
         self.dye_13_inc.image = tri_up
         self.dye_13_dec.image = tri_down

   def mark_change(self):
      self.has_changed = True
      self.statusVar.set(UNSAVED_CHANGES)
      self.statusBar.configure(fg="black")
   
   def increment_dye_0(self):
      val = self.dye_0_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_0_var.set(val + 8)
         self.changed_dyes.add(0)
         self.mark_change()

   def decrement_dye_0(self):
      val = self.dye_0_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_0_var.set(val - 8)
         self.changed_dyes.add(0)
         self.mark_change()

   def increment_dye_1(self):
      val = self.dye_1_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_1_var.set(val + 8)
         self.changed_dyes.add(1)
         self.mark_change()

   def decrement_dye_1(self):
      val = self.dye_1_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_1_var.set(val - 8)
         self.changed_dyes.add(1)
         self.mark_change()

   def increment_dye_2(self):
      val = self.dye_2_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_2_var.set(val + 8)
         self.changed_dyes.add(2)
         self.mark_change()

   def decrement_dye_2(self):
      val = self.dye_2_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_2_var.set(val - 8)
         self.changed_dyes.add(2)
         self.mark_change()

   def increment_dye_3(self):
      val = self.dye_3_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_3_var.set(val + 8)
         self.changed_dyes.add(3)
         self.mark_change()

   def decrement_dye_3(self):
      val = self.dye_3_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_3_var.set(val - 8)
         self.changed_dyes.add(3)
         self.mark_change()

   def increment_dye_4(self):
      val = self.dye_4_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_4_var.set(val + 8)
         self.changed_dyes.add(4)
         self.mark_change()

   def decrement_dye_4(self):
      val = self.dye_4_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_4_var.set(val - 8)
         self.changed_dyes.add(4)
         self.mark_change()

   def increment_dye_5(self):
      val = self.dye_5_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_5_var.set(val + 8)
         self.changed_dyes.add(5)
         self.mark_change()

   def decrement_dye_5(self):
      val = self.dye_5_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_5_var.set(val - 8)
         self.changed_dyes.add(5)
         self.mark_change()

   def increment_dye_6(self):
      val = self.dye_6_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_6_var.set(val + 8)
         self.changed_dyes.add(6)
         self.mark_change()

   def decrement_dye_6(self):
      val = self.dye_6_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_6_var.set(val - 8)
         self.changed_dyes.add(6)
         self.mark_change()

   def increment_dye_7(self):
      val = self.dye_7_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_7_var.set(val + 8)
         self.changed_dyes.add(7)
         self.mark_change()

   def decrement_dye_7(self):
      val = self.dye_7_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_7_var.set(val - 8)
         self.changed_dyes.add(7)
         self.mark_change()

   def increment_dye_8(self):
      val = self.dye_8_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_8_var.set(val + 8)
         self.changed_dyes.add(8)
         self.mark_change()

   def decrement_dye_8(self):
      val = self.dye_8_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_8_var.set(val - 8)
         self.changed_dyes.add(8)
         self.mark_change()

   def increment_dye_9(self):
      val = self.dye_9_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_9_var.set(val + 8)
         self.changed_dyes.add(9)
         self.mark_change()

   def decrement_dye_9(self):
      val = self.dye_9_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_9_var.set(val - 8)
         self.changed_dyes.add(9)
         self.mark_change()

   def increment_dye_10(self):
      val = self.dye_10_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_10_var.set(val + 8)
         self.changed_dyes.add(10)
         self.mark_change()

   def decrement_dye_10(self):
      val = self.dye_10_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_10_var.set(val - 8)
         self.changed_dyes.add(10)
         self.mark_change()

   def increment_dye_11(self):
      val = self.dye_11_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_11_var.set(val + 8)
         self.changed_dyes.add(11)
         self.mark_change()

   def decrement_dye_11(self):
      val = self.dye_11_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_11_var.set(val - 8)
         self.changed_dyes.add(11)
         self.mark_change()

   def increment_dye_12(self):
      val = self.dye_12_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_12_var.set(val + 8)
         self.changed_dyes.add(12)
         self.mark_change()

   def decrement_dye_12(self):
      val = self.dye_12_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_12_var.set(val - 8)
         self.changed_dyes.add(12)
         self.mark_change()

   def increment_dye_13(self):
      val = self.dye_13_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_13_var.set(val + 8)
         self.changed_dyes.add(13)
         self.mark_change()

   def decrement_dye_13(self):
      val = self.dye_13_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_13_var.set(val - 8)
         self.changed_dyes.add(13)
         self.mark_change()

   def validate_gap_value(self, num):
      try:
         num = int(num)
      except:
         return 0
      if num in GAP_VALUE_RANGE:
         return num
      if num > 200:
         return 200
      if num < -200:
         return -200
      for i in GAP_VALUE_RANGE:
         if i > num:
            return i

   def load_APA_file(self):
      sys_drive = os.getenv("SYSTEMDRIVE")
      if not sys_drive:
         sys_drive = "C:"
      sys_drive = os.path.join(sys_drive)
      path = filedialog.askopenfilename(title = "Load apa_data.pcl file", initialdir=sys_drive, filetypes = [("APA Data File", "*.pcl")])
      if path:
         if self.parse_APA_file(path):
            self.save_button["state"] = "normal"
            self.dye_0_lab.configure(fg="blue")
            self.dye_1_lab.configure(fg="blue")
            self.dye_2_lab.configure(fg="blue")
            self.dye_3_lab.configure(fg="blue")
            self.dye_4_lab.configure(fg="blue")
            self.dye_5_lab.configure(fg="blue")
            self.dye_6_lab.configure(fg="blue")
            self.dye_7_lab.configure(fg="blue")
            self.dye_8_lab.configure(fg="blue")
            self.dye_9_lab.configure(fg="blue")
            self.dye_10_lab.configure(fg="blue")
            self.dye_11_lab.configure(fg="blue")
            self.dye_12_lab.configure(fg="blue")
            self.dye_13_lab.configure(fg="blue")
            self.dye_0_inc["state"] = "normal"
            self.dye_0_dec["state"] = "normal"
            self.dye_1_inc["state"] = "normal"
            self.dye_1_dec["state"] = "normal"
            self.dye_2_inc["state"] = "normal"
            self.dye_2_dec["state"] = "normal"
            self.dye_3_inc["state"] = "normal"
            self.dye_3_dec["state"] = "normal"
            self.dye_4_inc["state"] = "normal"
            self.dye_4_dec["state"] = "normal"
            self.dye_5_inc["state"] = "normal"
            self.dye_5_dec["state"] = "normal"
            self.dye_6_inc["state"] = "normal"
            self.dye_6_dec["state"] = "normal"
            self.dye_7_inc["state"] = "normal"
            self.dye_7_dec["state"] = "normal"
            self.dye_8_inc["state"] = "normal"
            self.dye_8_dec["state"] = "normal"
            self.dye_9_inc["state"] = "normal"
            self.dye_9_dec["state"] = "normal"
            self.dye_10_inc["state"] = "normal"
            self.dye_10_dec["state"] = "normal"
            self.dye_11_inc["state"] = "normal"
            self.dye_11_dec["state"] = "normal"
            self.dye_12_inc["state"] = "normal"
            self.dye_12_dec["state"] = "normal"
            self.dye_13_inc["state"] = "normal"
            self.dye_13_dec["state"] = "normal"
            self.statusBar.configure(fg="blue")
            self.statusVar.set(FILE_LOAD_SUCCESSFULL)

   def parse_APA_file(self, path):
      if not os.path.exists(path):
         return False
      dye_values = {}
      with open(path, "r") as f:
         for xmlfile in f.read().split("\n\n"):
            if "?xml" in xmlfile:
               dom = parseXMLString(xmlfile)
               for iparam in dom.getElementsByTagName("ompcapn:InputParam"):
                  children = iparam.childNodes
                  if children:
                     node = children[0]
                     if node.nodeType == node.TEXT_NODE and "oem_set_alignment_values" in node.data:
                        values = node.data.replace("oem_set_alignment_values", "").replace(" ", "").split(",")
                        if values[0] == "0" and values[3] == "0":
                           try:
                              dye_values[int(values[2])] = int(values[4])
                           except:
                              return False
      if len(dye_values) != 14:
         return False
      for dye, value in dye_values.items():
         if dye == 0:
            self.dye_0_var.set(self.validate_gap_value(value))
         elif dye == 1:
            self.dye_1_var.set(self.validate_gap_value(value))
         elif dye == 2:
            self.dye_2_var.set(self.validate_gap_value(value))
         elif dye == 3:
            self.dye_3_var.set(self.validate_gap_value(value))
         elif dye == 4:
            self.dye_4_var.set(self.validate_gap_value(value))
         elif dye == 5:
            self.dye_5_var.set(self.validate_gap_value(value))
         elif dye == 6:
            self.dye_6_var.set(self.validate_gap_value(value))
         elif dye == 7:
            self.dye_7_var.set(self.validate_gap_value(value))
         elif dye == 8:
            self.dye_8_var.set(self.validate_gap_value(value))
         elif dye == 9:
            self.dye_9_var.set(self.validate_gap_value(value))
         elif dye == 10:
            self.dye_10_var.set(self.validate_gap_value(value))
         elif dye == 11:
            self.dye_11_var.set(self.validate_gap_value(value))
         elif dye == 12:
            self.dye_12_var.set(self.validate_gap_value(value))
         elif dye == 13:
            self.dye_13_var.set(self.validate_gap_value(value))
      return True

   def update_dye(self, dye):
      if dye < 0 or 13 < dye:
         return False
      dye_value = self.dye_vars[dye].get()
      for color in range(0, 4):
         if not set_dye(dye, color, dye_value):
            return False
         sleep(0.1)
      return True

   def save_changes(self):
      if not self.has_changed or not self.filepath:
         return
      for dye in self.changed_dyes:
         if not self.update_dye(dye):
            self.statusVar.set(FILE_SAVE_UNSUCCESSFULL)
            self.statusBar.configure(fg="red")
            return
      if not check_status():
         return
      self.changed_dyes = set()
      self.has_changed = False
      self.statusVar.set(FILE_SAVE_SUCCESSFULL)
      self.statusBar.configure(fg="blue")

   def mainloop(self):
      self.root.mainloop()

if __name__ == "__main__":
   DGATool = DyeGapAdjustmentTool()
   DGATool.mainloop()
