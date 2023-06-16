#!/usr/bin/python3
# Author: Ronny Toribio
# Project: Dye Gap Adjustment Tool
# Description: A dye gap adjustment tool that edits the apa_data.pcl file.
import os
import os.path

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

DEFAULT_STATUS = " Please load the apa_data.pcl file."
FILE_LOAD_SUCCESSFULL = " The apa_data.pcl file was loaded successfully."
FILE_SAVE_SUCCESSFULL = " The apa_data.pcl file was saved successfully."
UNSAVED_CHANGES = " There are unsaved changes."

APA_FILE = "%Pcal_pg.set_pa_value_res 0,0,0,0,{},1200;cal_pg.set_pa_value_res 0,0,0,1,{},1200;cal_pg.set_pa_value_res 0,0,0,2,{},1200;cal_pg.set_pa_value_res 0,0,0,3,{},1200;cal_pg.set_pa_value_res 0, 0,1,0,{},19200;cal_pg.set_pa_value_res 0, 0,1,1,{},19200;cal_pg.set_pa_value_res 0, 0,1,2,{},19200;cal_pg.set_pa_value_res 0, 0,1,3,{},19200;cal_pg.set_pa_value_res 0, 0,2,0,{},19200;cal_pg.set_pa_value_res 0, 0,2,1,{},19200;cal_pg.set_pa_value_res 0, 0,2,2,{},19200;cal_pg.set_pa_value_res 0, 0,2,3,{},19200;cal_pg.set_pa_value_res 0, 0,3,0,{},19200;cal_pg.set_pa_value_res 0, 0,3,1,{},19200;cal_pg.set_pa_value_res 0, 0,3,2,{},19200;cal_pg.set_pa_value_res 0, 0,3,3,{},19200;cal_pg.set_pa_value_res 0, 0,4,0,{},19200;cal_pg.set_pa_value_res 0, 0,4,1,{},19200;cal_pg.set_pa_value_res 0, 0,4,2,{},19200;cal_pg.set_pa_value_res 0, 0,4,3,{},19200;cal_pg.set_pa_value_res 0, 0,5,0,{},19200;cal_pg.set_pa_value_res 0, 0,5,1,{},19200;cal_pg.set_pa_value_res 0, 0,5,2,{},19200;cal_pg.set_pa_value_res 0, 0,5,3,{},19200;cal_pg.set_pa_value_res 0, 0,6,0,{},19200;cal_pg.set_pa_value_res 0, 0,6,1,{},19200;cal_pg.set_pa_value_res 0, 0,6,2,{},19200;cal_pg.set_pa_value_res 0, 0,6,3,{},19200;cal_pg.set_pa_value_res 0, 0,7,0,{},19200;cal_pg.set_pa_value_res 0, 0,7,1,{},19200;cal_pg.set_pa_value_res 0, 0,7,2,{},19200;cal_pg.set_pa_value_res 0, 0,7,3,{},19200;cal_pg.set_pa_value_res 0, 0,8,0,{},19200;cal_pg.set_pa_value_res 0, 0,8,1,{},19200;cal_pg.set_pa_value_res 0, 0,8,2,{},19200;cal_pg.set_pa_value_res 0, 0,8,3,{},19200;cal_pg.set_pa_value_res 0, 0,9,0,{},19200;cal_pg.set_pa_value_res 0, 0,9,1,{},19200;cal_pg.set_pa_value_res 0, 0,9,2,{},19200;cal_pg.set_pa_value_res 0, 0,9,3,{},19200;cal_pg.set_pa_value_res 0, 0,10,0,{},19200;cal_pg.set_pa_value_res 0, 0,10,1,{},19200;cal_pg.set_pa_value_res 0, 0,10,2,{},19200;cal_pg.set_pa_value_res 0, 0,10,3,{},19200;cal_pg.set_pa_value_res 0, 0,11,0,{},19200;cal_pg.set_pa_value_res 0, 0,11,1,{},19200;cal_pg.set_pa_value_res 0, 0,11,2,{},19200;cal_pg.set_pa_value_res 0, 0,11,3,{},19200;cal_pg.set_pa_value_res 0, 0,12,0,{},19200;cal_pg.set_pa_value_res 0, 0,12,1,{},19200;cal_pg.set_pa_value_res 0, 0,12,2,{},19200;cal_pg.set_pa_value_res 0, 0,12,3,{},19200;cal_pg.set_pa_value_res 0, 0,13,0,{},19200;cal_pg.set_pa_value_res 0, 0,13,1,{},19200;cal_pg.set_pa_value_res 0, 0,13,2,{},19200;cal_pg.set_pa_value_res 0, 0,13,3,{},19200;"
APA_FILE_2 = b"cal_pg.set_pa_value_res 1, 0,0,0,0,2400;cal_pg.set_pa_value_res 1, 0,0,1,0,2400;cal_pg.set_pa_value_res 1, 0,0,2,0,2400;cal_pg.set_pa_value_res 1, 0,0,3,0,2400;cal_pg.set_pa_value_res 1, 0,1,0,-4,19200;cal_pg.set_pa_value_res 1, 0,1,1,-4,19200;cal_pg.set_pa_value_res 1, 0,1,2,-4,19200;cal_pg.set_pa_value_res 1, 0,1,3,-4,19200;cal_pg.set_pa_value_res 1, 0,2,0,-28,19200;cal_pg.set_pa_value_res 1, 0,2,1,-28,19200;cal_pg.set_pa_value_res 1, 0,2,2,-28,19200;cal_pg.set_pa_value_res 1, 0,2,3,-28,19200;cal_pg.set_pa_value_res 1, 0,3,0,4,19200;cal_pg.set_pa_value_res 1, 0,3,1,4,19200;cal_pg.set_pa_value_res 1, 0,3,2,4,19200;cal_pg.set_pa_value_res 1, 0,3,3,4,19200;cal_pg.set_pa_value_res 1, 0,4,0,17,19200;cal_pg.set_pa_value_res 1, 0,4,1,17,19200;cal_pg.set_pa_value_res 1, 0,4,2,17,19200;cal_pg.set_pa_value_res 1, 0,4,3,17,19200;cal_pg.set_pa_value_res 1, 0,5,0,-39,19200;cal_pg.set_pa_value_res 1, 0,5,1,-39,19200;cal_pg.set_pa_value_res 1, 0,5,2,-39,19200;cal_pg.set_pa_value_res 1, 0,5,3,-39,19200;cal_pg.set_pa_value_res 1, 0,6,0,7,19200;cal_pg.set_pa_value_res 1, 0,6,1,7,19200;cal_pg.set_pa_value_res 1, 0,6,2,7,19200;cal_pg.set_pa_value_res 1, 0,6,3,7,19200;cal_pg.set_pa_value_res 1, 0,7,0,-20,19200;cal_pg.set_pa_value_res 1, 0,7,1,-20,19200;cal_pg.set_pa_value_res 1, 0,7,2,-20,19200;cal_pg.set_pa_value_res 1, 0,7,3,-20,19200;cal_pg.set_pa_value_res 1, 0,8,0,34,19200;cal_pg.set_pa_value_res 1, 0,8,1,34,19200;cal_pg.set_pa_value_res 1, 0,8,2,34,19200;cal_pg.set_pa_value_res 1, 0,8,3,34,19200;cal_pg.set_pa_value_res 1, 0,9,0,-28,19200;cal_pg.set_pa_value_res 1, 0,9,1,-28,19200;cal_pg.set_pa_value_res 1, 0,9,2,-28,19200;cal_pg.set_pa_value_res 1, 0,9,3,-28,19200;cal_pg.set_pa_value_res 1, 0,10,0,12,19200;cal_pg.set_pa_value_res 1, 0,10,1,12,19200;cal_pg.set_pa_value_res 1, 0,10,2,12,19200;cal_pg.set_pa_value_res 1, 0,10,3,12,19200;cal_pg.set_pa_value_res 1, 0,11,0,-9,19200;cal_pg.set_pa_value_res 1, 0,11,1,-9,19200;cal_pg.set_pa_value_res 1, 0,11,2,-9,19200;cal_pg.set_pa_value_res 1, 0,11,3,-9,19200;cal_pg.set_pa_value_res 1, 0,12,0,16,19200;cal_pg.set_pa_value_res 1, 0,12,1,16,19200;cal_pg.set_pa_value_res 1, 0,12,2,16,19200;cal_pg.set_pa_value_res 1, 0,12,3,16,19200;cal_pg.set_pa_value_res 1, 0,13,0,-21,19200;cal_pg.set_pa_value_res 1, 0,13,1,-21,19200;cal_pg.set_pa_value_res 1, 0,13,2,-21,19200;cal_pg.set_pa_value_res 1, 0,13,3,-21,19200;cal_pg.commit_cal_values 0 0;sweep_mgr.refresh_masks;udw.quit;%-12345X"

GAP_VALUE_RANGE = [-200, -192, -184, -176, -168, -160, -152, -144, -136, -128, -120, -112, -104, -96, -88, -80, -72, -64, -56, -48, -40, -32, -24, -16, -8, 0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200]

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
      self.root.bind("<Control-o>", self.loadAPAFile2)
      self.root.bind("<Control-l>", self.loadAPAFile2)
      self.root.bind("<Control-s>", self.saveAPAFile2)

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

      # Dye 0 Panel
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

      # Dye 1 Panel
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

      # Dye 2 Panel
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

      # Dye 3 Panel
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

      # Dye 4 Panel
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

      # Dye 5 Panel
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

      # Dye 6 Panel
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

      # Dye 7 Panel
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

      # Dye 8 Panel
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

      # Dye 9 Panel
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

      # Dye 10 Panel
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

      # Dye 11 Panel
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

      # Dye 12 Panel
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

      # Dye 13 Panel
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

      # Operations
      self.load_button = tk.Button(self.button_panel, text="Load File", command=self.loadAPAFile)
      self.load_button.grid(column=0, row=6)
      self.save_button = tk.Button(self.button_panel, text="Apply Changes", command=self.saveAPAFile)
      self.save_button.grid(column=1, row=6)
      self.save_button["state"] = "disabled"

      # Button images
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
      
   def increment_dye_0(self):
      val = self.dye_0_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_0_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_0(self):
      val = self.dye_0_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_0_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_1(self):
      val = self.dye_1_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_1_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_1(self):
      val = self.dye_1_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_1_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_2(self):
      val = self.dye_2_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_2_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_2(self):
      val = self.dye_2_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_2_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_3(self):
      val = self.dye_3_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_3_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_3(self):
      val = self.dye_3_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_3_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_4(self):
      val = self.dye_4_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_4_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_4(self):
      val = self.dye_4_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_4_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_5(self):
      val = self.dye_5_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_5_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_5(self):
      val = self.dye_5_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_5_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_6(self):
      val = self.dye_6_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_6_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_6(self):
      val = self.dye_6_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_6_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_7(self):
      val = self.dye_7_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_7_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_7(self):
      val = self.dye_7_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_7_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_8(self):
      val = self.dye_8_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_8_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_8(self):
      val = self.dye_8_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_8_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_9(self):
      val = self.dye_9_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_9_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_9(self):
      val = self.dye_9_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_9_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_10(self):
      val = self.dye_10_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_10_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_10(self):
      val = self.dye_10_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_10_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_11(self):
      val = self.dye_11_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_11_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_11(self):
      val = self.dye_11_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_11_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_12(self):
      val = self.dye_12_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_12_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_12(self):
      val = self.dye_12_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_12_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def increment_dye_13(self):
      val = self.dye_13_var.get()
      if val in GAP_VALUE_RANGE and val < 200:
         self.dye_13_var.set(val + 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def decrement_dye_13(self):
      val = self.dye_13_var.get()
      if val in GAP_VALUE_RANGE and val > -200:
         self.dye_13_var.set(val - 8)
         self.has_changed = True
         self.statusVar.set(UNSAVED_CHANGES)

   def validateGapValue(self, num):
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

   def loadAPAFile(self):
      sys_drive = os.getenv("SYSTEMDRIVE")
      if not sys_drive:
         sys_drive = "C:"
      sys_drive = os.path.join(sys_drive)
      path = filedialog.askopenfilename(title = "Load apa_data.pcl file", initialdir=sys_drive, filetypes = [("APA Data File", "*.pcl")])
      if path:
         if self.parseAPAFile(path):
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
            self.statusVar.set(FILE_LOAD_SUCCESSFULL)
         else:
            messagebox.showwarning(title="File Error", message="Please load a correct apa_data.pcl file.")

   def loadAPAFile2(self, e):
      self.loadAPAFile()

   def parseAPAFile(self, path):
      if not os.path.exists(path):
         return False
      self.filepath = path
      with open(path, "rb") as f:
         contents = f.read()
         if not contents:
            return False
         dyes = contents.decode().split(";")
         if len(dyes) != 116:
            return False
         for i, dye in enumerate(dyes):
            dye = dye.split(",")
            if len(dye) != 6:
               return False
            if i == 0:
               self.dye_0_var.set(self.validateGapValue(dye[4]))
            elif i == 4:
               self.dye_1_var.set(self.validateGapValue(dye[4]))
            elif i == 8:
               self.dye_2_var.set(self.validateGapValue(dye[4]))
            elif i == 12:
               self.dye_3_var.set(self.validateGapValue(dye[4]))
            elif i == 16:
               self.dye_4_var.set(self.validateGapValue(dye[4]))
            elif i == 20:
               self.dye_5_var.set(self.validateGapValue(dye[4]))
            elif i == 24:
               self.dye_6_var.set(self.validateGapValue(dye[4]))
            elif i == 28:
               self.dye_7_var.set(self.validateGapValue(dye[4]))
            elif i == 32:
               self.dye_8_var.set(self.validateGapValue(dye[4]))
            elif i == 36:
               self.dye_9_var.set(self.validateGapValue(dye[4]))
            elif i == 40:
               self.dye_10_var.set(self.validateGapValue(dye[4]))
            elif i == 44:
               self.dye_11_var.set(self.validateGapValue(dye[4]))
            elif i == 48:
               self.dye_12_var.set(self.validateGapValue(dye[4]))
            elif i == 52:
               self.dye_13_var.set(self.validateGapValue(dye[4]))
               break
      return True

   def saveAPAFile(self):
      if not self.has_changed or not self.filepath:
         return
      with open(self.filepath, "wb") as f:
          f.write(APA_FILE.format(self.dye_0_var.get(), self.dye_0_var.get(), self.dye_0_var.get(), self.dye_0_var.get(),
                                  self.dye_1_var.get(), self.dye_1_var.get(), self.dye_1_var.get(), self.dye_1_var.get(),
                                  self.dye_2_var.get(), self.dye_2_var.get(), self.dye_2_var.get(), self.dye_2_var.get(),
                                  self.dye_3_var.get(), self.dye_3_var.get(), self.dye_3_var.get(), self.dye_3_var.get(),
                                  self.dye_4_var.get(), self.dye_4_var.get(), self.dye_4_var.get(), self.dye_4_var.get(),
                                  self.dye_5_var.get(), self.dye_5_var.get(), self.dye_5_var.get(), self.dye_5_var.get(),
                                  self.dye_6_var.get(), self.dye_6_var.get(), self.dye_6_var.get(), self.dye_6_var.get(),
                                  self.dye_7_var.get(), self.dye_7_var.get(), self.dye_7_var.get(), self.dye_7_var.get(),
                                  self.dye_8_var.get(), self.dye_8_var.get(), self.dye_8_var.get(), self.dye_8_var.get(),
                                  self.dye_9_var.get(), self.dye_9_var.get(), self.dye_9_var.get(), self.dye_9_var.get(),
                                  self.dye_10_var.get(), self.dye_10_var.get(), self.dye_10_var.get(), self.dye_10_var.get(),
                                  self.dye_11_var.get(), self.dye_11_var.get(), self.dye_11_var.get(), self.dye_11_var.get(),
                                  self.dye_12_var.get(), self.dye_12_var.get(), self.dye_12_var.get(), self.dye_12_var.get(),
                                  self.dye_13_var.get(), self.dye_13_var.get(), self.dye_13_var.get(), self.dye_13_var.get()).encode())
          f.write(APA_FILE_2)
      self.has_changed = False
      self.statusVar.set(FILE_SAVE_SUCCESSFULL)

   def saveAPAFile2(self, e):
      self.saveAPAFile()

   def mainloop(self):
      self.root.mainloop()

if __name__ == "__main__":
   DGATool = DyeGapAdjustmentTool()
   DGATool.mainloop()
