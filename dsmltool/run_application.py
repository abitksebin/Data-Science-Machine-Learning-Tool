# !python3
# -------------------------------------------------------------------------------
# Name:        data_process.py
# Purpose:     Data Process Tab code of the tool
# Project:     dsmltool - BITS M.Tech Dissertation
# Author:      Abit K Sebin
#
# Created:     Jun - Aug 2022
# Copyright:   (c) abitk 2022
# Licence:     <None>
# -------------------------------------------------------------------------------

import time
import tkinter as tk
from functools import partial
from tkinter import LEFT
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk

import win32con  # used for hiding console
import win32gui  # used for hiding console

import configurable_constants
import data_analysis
import data_process
import feature_selection
import ml_classification
import ml_clustering
import ml_predict
import ml_regression
from common_functions_helper import Helper
from extra_styling_classes import Splash, WelcomeScreen

# --------------------------------------------------------------------
helper_object = Helper.getInstance()
SW_version = configurable_constants.SW_VER
SW_TITLE = configurable_constants.SW_TITLE
log = helper_object.get_logger()

# Hide console if configured
if helper_object.get_configuration().getboolean('RUN', 'HIDE_CONSOLE'):
    The_program_to_hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(The_program_to_hide, win32con.SW_HIDE)


class App(tk.Tk):
    """Application root class which controls the entire application"""

    def __init__(self):
        tk.Tk.__init__(self)
        self.withdraw()
        if helper_object.get_configuration().getboolean('RUN', 'SPLASH_ON'):
            splash = Splash(self)
            time.sleep(configurable_constants.SPLASH_DELAY)  # simulate a delay while loading splash
        root = self
        root.title(configurable_constants.SW_TITLE)
        root.geometry("1024x768+20+5")
        root.minsize(1024, 768)
        self.title(SW_TITLE)
        # Theme styling for Tabs and window
        self.apply_theme_for_tabs()

        # creating tabs
        tab_parent = ttk.Notebook(root)
        tab_parent.configure(height=725)
        tab_data_process = ttk.Frame(tab_parent)
        tab_data_analysis = ttk.Frame(tab_parent)
        tab_feature_selection = ttk.Frame(tab_parent)
        tab_ml_classification = ttk.Frame(tab_parent)
        tab_ml_clustering = ttk.Frame(tab_parent)
        tab_ml_regression = ttk.Frame(tab_parent)
        tab_ml_predict = ttk.Frame(tab_parent)
        tab_parent.add(tab_data_process, text="Data Processing")
        tab_parent.add(tab_data_analysis, text="Data Analysis")
        tab_parent.add(tab_feature_selection, text="Feature Selection")
        tab_parent.add(tab_ml_classification, text="ML Training - Classification")
        tab_parent.add(tab_ml_clustering, text="ML Training - Clustering")
        tab_parent.add(tab_ml_regression, text="ML Training - Regression")
        tab_parent.add(tab_ml_predict, text="ML Prediction")
        tab_parent.bind('<<NotebookTabChanged>>', self.tab_change_event)
        tab_parent.pack(expand=1, fill='both')

        # WelcomeScreen
        if helper_object.get_configuration().getboolean('RUN', 'WELCOME_ON'):
            WelcomeScreen(self)
        # destroy splash when finished loading
        if helper_object.get_configuration().getboolean('RUN', 'SPLASH_ON'):
            splash.destroy()
        helper_object.set_data_process_obj(data_process.DataProcess(tab_data_process))
        helper_object.set_data_analysis_obj(data_analysis.DataAnalysis(tab_data_analysis))
        helper_object.set_feature_selection_obj(feature_selection.FeatureSelection(tab_feature_selection))
        helper_object.set_ml_classification_obj(ml_classification.MlClassification(tab_ml_classification))
        helper_object.set_ml_clustering_obj(ml_clustering.MlClustering(tab_ml_clustering))
        helper_object.set_ml_regression_obj(ml_regression.MlRegression(tab_ml_regression))
        helper_object.set_ml_predict_obj(ml_predict.MlPrediction(tab_ml_predict))

        # footer
        self.frame_footer = tk.Frame(root, borderwidth=0, highlightthickness=0, highlightbackground="yellow")
        self.frame_footer.pack(side=LEFT, pady=0)
        helper_object.label_footer_status_label = tk.Label(self.frame_footer, text="INFO:")
        helper_object.label_footer_status_label.pack(side=LEFT)
        helper_object.label_footer_df_status = tk.Label(self.frame_footer,
                                                        text="Data not loaded. Please a load data file to start.")
        helper_object.label_footer_df_status.pack(side=LEFT)
        self.add_tool_menu()
        self.deiconify()

    def add_tool_menu(self):
        """Code for tool menu"""
        tool_menu_bar = Menu(self)
        self.config(menu=tool_menu_bar)
        file_menu = Menu(tool_menu_bar, tearoff=0)
        settings_menu = Menu(tool_menu_bar, tearoff=0)
        themes_menu = Menu(settings_menu, tearoff=0)
        help_menu = Menu(tool_menu_bar, tearoff=0)
        themes_menu.add_command(label="Theme 1", command=partial(self.switch_tab_theme, "theme_1"))
        themes_menu.add_command(label="Theme 2", command=partial(self.switch_tab_theme, "theme_2"))
        themes_menu.add_command(label="Default", command=partial(self.switch_tab_theme, "theme_3"))

        file_menu.add_command(label="Exit", underline=0, command=self.quit)
        help_menu.add_command(label="About", underline=0, command=self.show_about)
        tool_menu_bar.add_cascade(label="File", underline=0, menu=file_menu)
        tool_menu_bar.add_cascade(label="Settings", underline=0, menu=settings_menu)
        tool_menu_bar.add_cascade(label="Help", underline=0, menu=help_menu)
        settings_menu.add_cascade(label="Tab Colour Themes", menu=themes_menu)

    def tab_change_event(self, event):
        tab = event.widget.tab('current')['text']
        if tab == 'Data Analysis' or tab == 'Feature Selection':
            if helper_object.get_dframe().empty:
                pass
                messagebox.showerror("Data Frame Empty",
                                     "The data frame is empty. Please select CSV file(s) and load it using the Load Data button.")
            else:

                helper_object.get_data_analysis_obj().update_column_list_in_ctrl()
                helper_object.get_feature_selection_obj().update_column_list_in_ctrl()

    def show_about(self):
        WelcomeScreen(self)

    def apply_theme_for_tabs(self):
        dict_custom_themes = {
            "theme_1": {
                "TNotebook.Tab": {
                    "configure": {"background": configurable_constants.NONACTIVE_TAB_BG_COLOR,
                                  "foreground": "white"},
                    "map": {"background": [("selected", configurable_constants.ACTIVE_TAB_BG_COLOR)],
                            "expand": [("selected", [1, 1, 1, 0])]}
                },
                "TFrame": {"configure": {"background": "SystemButtonFace"}}
            },
            "theme_2": {
                "TNotebook.Tab": {
                    "configure": {"background": "white",
                                  "foreground": "Black"},
                    "map": {"background": [("selected", "green")],
                            "expand": [("selected", [1, 1, 1, 0])]}
                },
                "TFrame": {"configure": {"background": "SystemButtonFace"}}
            },
            "theme_3": {
                "TNotebook.Tab": {
                    "map": {"background": [("selected", "grey")],
                            }
                },
                "TFrame": {"configure": {"background": "SystemButtonFace"}}
            }
        }
        self.style = ttk.Style()
        self.style.theme_create("theme_1", settings=dict_custom_themes.get("theme_1"))
        self.style.theme_create("theme_2", settings=dict_custom_themes.get("theme_2"))
        self.style.theme_create("theme_3", settings=dict_custom_themes.get("theme_3"))
        self.style.theme_use("theme_3")

    def switch_tab_theme(self, custom_theme="theme_1"):
        self.style.theme_use(custom_theme)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
