# -------------------------------------------------------------------------------
# Name:        extra_styling_classes.py
# Purpose:     code for extra styling like splash screen, welcome screen
# Project:     dsmltool - BITS M.Tech Dissertation
# Author:      Abit K Sebin
#
# Created:     Jun - Aug 2022
# Copyright:   (c) abitk 2022
# Licence:     <None>
# -------------------------------------------------------------------------------
import tkinter as tk
from functools import partial
from tkinter import LEFT, RIGHT, X, BOTTOM

import configurable_constants
from common_functions_helper import Helper


class Splash(tk.Toplevel):
    """Class for splash screen """

    def __init__(self, parent):
        splashBgColor = "Black"
        splashTxtColor = "white"
        tk.Toplevel.__init__(self, parent)
        welcome = self
        welcome.overrideredirect(1)
        welcome.configure(bg=splashBgColor)
        welcome.geometry("650x200+250+200")
        welcome_frame1 = tk.Frame(welcome, bg=splashBgColor)
        welcome_frame1.pack(fill=X)
        label_welcome = tk.Label(welcome_frame1, text=configurable_constants.SW_TITLE, font=('Arial', 20, ' bold'),
                                 bg=splashBgColor, fg=splashTxtColor)
        label_welcome.pack(pady=20)
        welcome_frame2 = tk.Frame(welcome, bg=splashBgColor)
        welcome_frame2.pack(fill=X)
        label_welcome_version = tk.Label(welcome_frame2, text="Version: " + configurable_constants.SW_VER,
                                         font='Fixedsys 12', bg=splashBgColor, fg=splashTxtColor)
        label_welcome_version.pack(side=RIGHT, padx=30)
        label_welcome_text = tk.Label(welcome, text="LOADING...", font=('Arial', 14), justify=LEFT, bg=splashBgColor,
                                      fg=splashTxtColor)
        label_welcome_text.pack(pady=20)
        ## required to make window show before the program gets to the mainloop
        self.update()
        welcome.attributes('-topmost', True)


class WelcomeScreen(tk.Toplevel):
    """Class for welcome screen """
    welcome = None

    def welcome_close(self):
        hlp_obj = Helper.getInstance()
        if (self.var_show_welcome.get() == 1):
            hlp_obj.get_configuration().set('RUN', 'WELCOME_ON', 'False')
            hlp_obj.write_configuration_file()
        self.destroy()

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        welcome = self
        welcome.overrideredirect(1)
        welcome.configure(bg="Grey")
        welcome.geometry("700x500+250+200")
        welcome_frame1 = tk.Frame(welcome, bg="Grey")
        welcome_frame1.pack(fill=X)
        label_welcome = tk.Label(welcome_frame1, text=configurable_constants.SW_TITLE, font=('Arial', 22, ' bold'),
                                 bg="Grey",
                                 fg="white")
        label_welcome.pack(pady=20)
        welcome_frame2 = tk.Frame(welcome, bg="Grey")
        welcome_frame2.pack(fill=X)
        label_welcome_version = tk.Label(welcome_frame2, text="Version: " + configurable_constants.SW_VER,
                                         font='Fixedsys 12',
                                         bg="Grey", fg="white")
        label_welcome_version.pack(side=RIGHT, padx=30)
        label_welcome_text = tk.Label(welcome, text=configurable_constants.WELCOME_TEXT, font=('Arial', 10),
                                      justify=LEFT,
                                      bg="Grey", fg="white", wraplength=450)
        label_welcome_text.pack(pady=20)
        self.var_show_welcome = tk.IntVar()
        self.var_show_welcome.set(0)
        checkbutton_show_welcome = tk.Checkbutton(welcome, text="Don't show welcome screen when program starts",
                                                  variable=self.var_show_welcome, bg="Grey", fg="white",
                                                  selectcolor="grey")
        checkbutton_show_welcome.pack(side=BOTTOM)
        button_welcome_close = tk.Button(welcome, text="Close",
                                         command=partial(WelcomeScreen.welcome_close, self), width=20, height=2,
                                         bg="white")
        button_welcome_close.pack(side=BOTTOM, pady=10)
        welcome.attributes('-topmost', True)
