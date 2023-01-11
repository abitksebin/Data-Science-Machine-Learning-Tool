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
import datetime
import io
import os
import subprocess
import sys
import time
import tkinter as tk
from functools import partial
from tkinter import END, LEFT, RIGHT, X, Y, ACTIVE, messagebox, filedialog, INSERT, Text, BOTH, DISABLED, NORMAL

import pandas as pd
from tabulate import tabulate

import configurable_constants
from common_functions_helper import Helper

log = Helper.getInstance().get_logger()
helper_object_dp = Helper.getInstance()


class DataProcess:
    """Class that has all UI components and variables for Data Process Tab """

    def __init__(self, tab_data_process):
        self.DELIMITER = configurable_constants.DELIMITER
        self.tab_data_process = tab_data_process
        self.frame_section1 = tk.Frame(tab_data_process, borderwidth=0, highlightcolor="green", relief="solid",
                                       highlightthickness=0)
        self.frame_section1.pack(fill=X)
        self.base_path = os.path.dirname(sys.argv[0])
        self.outlier_column_list = []
        self.dframe = helper_object_dp.get_dframe()
        # --------section 1 Load Data----------------------------------------------------------------------------------------------------------------------------------------------
        self.labelframe_inputs = tk.LabelFrame(self.frame_section1, text="Load Data")
        self.labelframe_inputs.pack(padx=10, pady=5, ipady=2, fill=X)
        self.frame_section1_info = tk.Frame(self.labelframe_inputs, borderwidth=0, relief="sunken",
                                            highlightthickness=0, highlightbackground="black")
        self.frame_section1_info.pack(fill=X)
        self.frame_section1_layer1 = tk.Frame(self.labelframe_inputs, borderwidth=0, relief="sunken",
                                              highlightthickness=0, highlightbackground="red")
        self.frame_section1_layer1.pack(pady=0, padx=10, ipadx=1)
        self.frame_section1_layer2 = tk.Frame(self.labelframe_inputs, borderwidth=0, relief="sunken",
                                              highlightthickness=0, highlightbackground="blue")
        self.frame_section1_layer2.pack(pady=8, fill=X, ipadx=1)
        self.frame_section1_layer3 = tk.LabelFrame(self.labelframe_inputs, text="Data Cleaning Options (On Load)")
        self.frame_section1_layer3.pack(fill=X, ipady=5, pady=3, padx=15)

        self.label_info_ip = tk.Label(self.frame_section1_info, font='Helvetica 8 italic',
                                      text=" Select CSV type, select file(s), check required cleaning options and click on Load Data button.")
        self.label_info_ip.pack(anchor="w", side=LEFT)
        self.button_info_ip = tk.Button(self.frame_section1_info, font='Helvetica 8 italic', text="Help", fg="white",
                                        bg="grey", borderwidth=0, command=self.showinputinfo)
        self.button_info_ip.pack(side=RIGHT, anchor="n")
        self.var_inputtype = tk.IntVar()
        self.var_inputtype.set(1)
        self.label_csv_type = tk.Label(self.frame_section1_layer1, text="Select CSV Type:").pack(side=LEFT, padx=10)
        self.radio_inputtype = tk.Radiobutton(self.frame_section1_layer1,
                                              text="Data with same column headers (combines vertically)", padx=20,
                                              variable=self.var_inputtype, value=1).pack(side=LEFT)
        self.radio_inputtype = tk.Radiobutton(self.frame_section1_layer1,
                                              text="Data with different column headers (combines horizontally)",
                                              padx=20, variable=self.var_inputtype, value=2).pack(side=LEFT)

        self.frame_section1_ls = tk.Frame(self.frame_section1_layer2, borderwidth=0, relief="sunken",
                                          highlightthickness=0, highlightbackground="red")
        self.frame_section1_ls.pack(pady=0, padx=10, side=LEFT, ipadx=1)
        self.frame_section1_mid = tk.Frame(self.frame_section1_layer2, borderwidth=0, relief="sunken",
                                           highlightthickness=0, highlightbackground="blue")
        self.frame_section1_mid.pack(pady=0, padx=10, side=LEFT)
        self.frame_section1_rs = tk.Frame(self.frame_section1_layer2, borderwidth=0, relief="sunken",
                                          highlightthickness=0, highlightbackground="blue")
        self.frame_section1_rs.pack(pady=0, padx=10, side=LEFT)
        self.label_ip_fol = tk.Label(self.frame_section1_ls, text='Selected Files')
        self.label_ip_fol.pack(padx=0)
        self.frame_listbox = tk.Frame(self.frame_section1_ls, highlightthickness=0, highlightbackground="blue")
        self.frame_listbox.pack(side=LEFT, pady=0, padx=3)
        self.scrollbar = tk.Scrollbar(self.frame_listbox)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox_files = tk.Listbox(self.frame_listbox, width=70, height=6, yscrollcommand=self.scrollbar.set)
        self.listbox_files.pack(padx=2)
        self.scrollbar.config(command=self.listbox_files.yview)
        self.browse_folder_button = tk.Button(self.frame_section1_mid, text="Add Files", height=1, width=20,
                                              command=self.browsefunc)  # command = browsefunc
        self.browse_folder_button.pack(pady=2)
        self.clear_button = tk.Button(self.frame_section1_mid, text="Remove Selected File", height=1, width=20,
                                      command=self.deleteFromItems)  # command = deleteFromItems
        self.clear_button.pack(pady=2)
        self.button_input_clearall = tk.Button(self.frame_section1_mid, text="Remove All Files", height=1, width=20,
                                               command=self.deleteAllFromItems)  # command = new
        self.button_input_clearall.pack(pady=2)
        self.load_header_button = tk.Button(self.frame_section1_mid, text="View Column Headers", height=1, width=20,
                                            command=self.loadheaders)  # command = loadheaders
        self.load_header_button.pack(pady=2)
        self.label_columnlist = tk.Label(self.frame_section1_rs, text='Column headers available in the file(s)')
        self.label_columnlist.pack(padx=3)
        self.text_columnlist = tk.Text(self.frame_section1_rs, height=5, width=35)
        self.text_columnlist.pack(padx=3)

        self.var_dropemptycolumns = tk.IntVar()
        self.var_dropemptycolumns.set(1)
        self.checkbutton_dropemptycolumns = tk.Checkbutton(self.frame_section1_layer3, text="Drop blank columns",
                                                           variable=self.var_dropemptycolumns, width=18)
        self.checkbutton_dropemptycolumns.pack(side=LEFT)
        self.var_dropblankrows = tk.IntVar()
        self.var_dropblankrows.set(1)
        self.checkbutton_dropblankrows = tk.Checkbutton(self.frame_section1_layer3, text="Drop blank rows",
                                                        variable=self.var_dropblankrows)
        self.checkbutton_dropblankrows.pack(side=LEFT)
        self.var_dropblankrowswithcolum1data = tk.IntVar()
        self.var_dropblankrowswithcolum1data.set(0)  # temporary disabling

        self.var_dropduplicatelines = tk.IntVar()
        self.var_dropduplicatelines.set(1)
        self.checkbutton_dropduplicatelines = tk.Checkbutton(self.frame_section1_layer3, text="Drop duplicate rows",
                                                             variable=self.var_dropduplicatelines, width=20)
        self.checkbutton_dropduplicatelines.pack(side=LEFT)

        # --imputation
        self.frame_section1_layer3_missing_values = tk.LabelFrame(self.frame_section1_layer3)
        self.frame_section1_layer3_missing_values.pack(side=LEFT)
        self.var_fill_nan_onload = tk.IntVar()
        self.var_fill_nan_onload.set(1)
        self.checkbutton_fill_onload = tk.Checkbutton(self.frame_section1_layer3_missing_values,
                                                      text="Treat missing values by", variable=self.var_fill_nan_onload,
                                                      width=20, command=self.enable_impute_options_onload)
        self.checkbutton_fill_onload.pack(side=LEFT)
        self.var_fill_nan_method = tk.IntVar()
        self.var_fill_nan_method.set(1)
        self.radio_fill_nan_method1 = tk.Radiobutton(self.frame_section1_layer3_missing_values,
                                                     text="Mean",
                                                     variable=self.var_fill_nan_method, value=1)
        self.radio_fill_nan_method1.pack(side=LEFT)
        self.radio_fill_nan_method2 = tk.Radiobutton(self.frame_section1_layer3_missing_values,
                                                     text="Median",
                                                     variable=self.var_fill_nan_method, value=2)
        self.radio_fill_nan_method2.pack(side=LEFT)
        self.radio_fill_nan_method3 = tk.Radiobutton(self.frame_section1_layer3_missing_values,
                                                     text="Mode",
                                                     variable=self.var_fill_nan_method, value=3)
        self.radio_fill_nan_method3.pack(side=LEFT)
        self.radio_fill_nan_method4 = tk.Radiobutton(self.frame_section1_layer3_missing_values,
                                                     text="Zero",
                                                     variable=self.var_fill_nan_method, value=4)
        self.radio_fill_nan_method4.pack(side=LEFT)
        self.radio_fill_nan_method5 = tk.Radiobutton(self.frame_section1_layer3_missing_values,
                                                     text="Delete rows",
                                                     variable=self.var_fill_nan_method, value=5)
        self.radio_fill_nan_method5.pack(side=LEFT)

        self.frame_loaddata = tk.Frame(self.labelframe_inputs)
        self.frame_loaddata.pack(padx=10, side=LEFT, fill=X)
        self.label_df_status_label = tk.Label(self.frame_loaddata, text="Data Load Status:", width=13)
        self.label_df_status_label.pack(side=LEFT)
        self.label_df_status = tk.Label(self.frame_loaddata, text="DATA NOT LOADED", width=20, fg="red")
        self.label_df_status.pack(side=LEFT)
        self.combinedata_button = tk.Button(self.frame_loaddata, text="LOAD DATA", height=2, width=50,
                                            command=self.loadFiles)
        self.combinedata_button.pack(pady=5, side=RIGHT, ipadx=0, padx=20)
        self.var_ignore_loadwarning = tk.IntVar()
        self.checkbutton_ignore_loadwarning = tk.Checkbutton(self.frame_loaddata,
                                                             text="Ignore data errors (Force Load)",
                                                             variable=self.var_ignore_loadwarning)
        self.checkbutton_ignore_loadwarning.pack(side=LEFT, padx=10)

        # --------section: Outlier Removal-----------------------------------------------------------------------------------------------------------------------------------------
        self.frame_section3 = tk.Frame(tab_data_process, highlightthickness=0, highlightbackground="red")
        self.frame_section3.pack(fill=X)
        self.frame_section3_label = tk.LabelFrame(self.frame_section3, text="More Options")

        self.frame_section3_label.pack(padx=10, pady=2, ipady=5, fill=X)
        self.label_info_or = tk.Label(self.frame_section3_label, font='Helvetica 8 italic',
                                      text="Columns or Outliers in the selected columns in the data frame can be removed here. Missing data can be imputed for selected columns.")
        self.label_info_or.pack(anchor='w')

        self.frame_section3_summarybtnsection = tk.Frame(self.frame_section3_label, highlightthickness=0,
                                                         highlightbackground="green")
        self.frame_section3_summarybtnsection.pack(fill=X)

        self.button_view_summary = tk.Button(self.frame_section3_summarybtnsection, text="View Summary", height=1,
                                             width=20, command=self.view_data_summary)
        self.button_view_summary.pack(side=LEFT, pady=2, padx=10)
        self.button_view_summary_tranpose = tk.Button(self.frame_section3_summarybtnsection,
                                                      text="View Summary Transpose", height=1, width=24,
                                                      command=partial(self.view_data_summary, True))
        self.button_view_summary_tranpose.pack(side=LEFT, pady=2, padx=10)
        self.button_view_summary_tranpose = tk.Button(self.frame_section3_summarybtnsection, text="View Data Info",
                                                      height=1, width=24, command=self.view_data_info)
        self.button_view_summary_tranpose.pack(side=LEFT, pady=2, padx=10)
        self.button_view_sample_data = tk.Button(self.frame_section3_summarybtnsection, text="View Sample Data",
                                                 height=1, width=24, command=partial(self.view_data_head, 10))
        self.button_view_sample_data.pack(side=LEFT, pady=2, padx=10)
        self.button_view_data_types = tk.Button(self.frame_section3_summarybtnsection, text="View Data Types", height=1,
                                                width=24, command=self.view_data_types)
        self.button_view_data_types.pack(side=LEFT, pady=1, padx=10)
        self.button_info_outlier = tk.Button(self.frame_section3_label, font='Helvetica 8 italic', text="Help",
                                             command=self.showoutlierremovalinfo, fg="white", bg="grey", borderwidth=0)
        self.button_info_outlier.pack(side=RIGHT, anchor="n")

        self.frame_section3_OR = tk.Frame(self.frame_section3_label, borderwidth=0, highlightthickness=0,
                                          highlightbackground="blue")
        self.frame_section3_OR.pack(side=LEFT, padx=0, ipady=0, ipadx=0)
        self.frame_section3_line = tk.Frame(self.frame_section3_OR)
        self.frame_section3_line.pack(side=LEFT)
        self.frame_section3_ls = tk.Frame(self.frame_section3_line, borderwidth=0, highlightthickness=0,
                                          highlightbackground="blue")
        self.frame_section3_ls.pack(side=LEFT, padx=0)
        self.label_available_headers = tk.Label(self.frame_section3_ls, text="Columns available in the data")
        self.label_available_headers.pack()
        self.scrollbar_available_headers = tk.Scrollbar(self.frame_section3_ls)
        self.scrollbar_available_headers.pack(side=RIGHT, fill=Y)
        self.listbox_available_headers = tk.Listbox(self.frame_section3_ls, width=35, height=5,
                                                    yscrollcommand=self.scrollbar_available_headers.set)
        self.listbox_available_headers.pack(padx=20)
        self.scrollbar_available_headers.config(command=self.listbox_available_headers.yview)
        self.frame_section3_mid = tk.Frame(self.frame_section3_line, borderwidth=0, highlightthickness=0,
                                           highlightbackground="red")
        self.frame_section3_mid.pack(side=LEFT, padx=10)
        self.button_addto_outlierlist = tk.Button(self.frame_section3_mid, text="Add selected\t >", height=1, width=20,
                                                  command=self.addtoOutlierList)
        self.button_addto_outlierlist.pack(pady=1, padx=10)
        self.button_addallto_outlierlist = tk.Button(self.frame_section3_mid, text="Add all\t\t>>", height=1, width=20,
                                                     command=self.addalltoOutlierList)
        self.button_addallto_outlierlist.pack(pady=1, padx=10)
        self.button_removefrom_outlierlist = tk.Button(self.frame_section3_mid, text="Remove selected\t <", height=1,
                                                       width=20,
                                                       command=self.removefromOutlierList)
        self.button_removefrom_outlierlist.pack(pady=1, padx=10)
        self.button_removeallfrom_outlierlist = tk.Button(self.frame_section3_mid, text="Remove all\t<<", height=1,
                                                          width=20,
                                                          command=self.removeallfromOutlierList)
        self.button_removeallfrom_outlierlist.pack(pady=1, padx=10)
        self.frame_section3_rs = tk.Frame(self.frame_section3_line, borderwidth=0, highlightthickness=0,
                                          highlightbackground="green")
        self.frame_section3_rs.pack(side=LEFT, padx=10)
        self.label_outlierlist_headers = tk.Label(self.frame_section3_rs, text="Columns Selected for Operation")
        self.label_outlierlist_headers.pack()
        self.scrollbar_outlierlist_headers = tk.Scrollbar(self.frame_section3_rs)
        self.scrollbar_outlierlist_headers.pack(side=RIGHT, fill=Y)
        self.listbox_outlierlist_headers = tk.Listbox(self.frame_section3_rs, width=33, height=5,
                                                      yscrollcommand=self.scrollbar_outlierlist_headers.set)
        self.listbox_outlierlist_headers.pack(padx=0)
        self.scrollbar_outlierlist_headers.config(command=self.listbox_outlierlist_headers.yview)

        self.frame_section3_line_btn = tk.LabelFrame(self.frame_section3_line,
                                                     text="Operations available in the selected columns")
        self.frame_section3_line_btn.pack(side=LEFT, pady=5, padx=10)
        self.button_remove_outliers = tk.Button(self.frame_section3_line_btn, text="Remove Outliers",
                                                height=1, width=30, command=self.removeOutliers)
        self.button_remove_outliers.pack(pady=2)

        self.button_remove_columns = tk.Button(self.frame_section3_line_btn, text="Remove Columns", height=1,
                                               width=30, command=self.removeColumns)
        self.button_remove_columns.pack(pady=2)
        self.button_onehot_encode_category = tk.Button(self.frame_section3_line_btn, text="Onehot-encode Columns",
                                                       height=1,
                                                       width=30, command=self.onehot_encode_category_DP)
        self.button_onehot_encode_category.pack(pady=2)
        self.button_impute_null = tk.Button(self.frame_section3_line_btn, text="Fill missing values using", height=1,
                                            width=30, command=self.impute_selcted_columns)
        self.button_impute_null.pack()

        self.frame_section_impute = tk.Frame(self.frame_section3_line_btn, borderwidth=1, highlightthickness=0,
                                             highlightbackground="red")
        self.frame_section_impute.pack(fill=X, pady=0)
        self.var_impute_method = tk.IntVar()
        self.var_impute_method.set(1)
        tk.Radiobutton(self.frame_section_impute,
                       text="Mean", padx=5,
                       variable=self.var_impute_method, value=1).pack(side=LEFT)
        tk.Radiobutton(self.frame_section_impute,
                       text="Median", padx=5,
                       variable=self.var_impute_method, value=2).pack(side=LEFT)
        tk.Radiobutton(self.frame_section_impute,
                       text="Mode", padx=5,
                       variable=self.var_impute_method, value=3).pack(side=LEFT)

        # --------------Data Export---------------------------------------------------------------------------------------------------------------------------------------------------
        self.frame_section4 = tk.Frame(tab_data_process, borderwidth=1, highlightthickness=0,
                                       highlightbackground="black")
        self.frame_section4.pack(fill=X, ipady=5)
        self.frame_save = tk.LabelFrame(self.frame_section4, text="Export Processed Data")
        self.frame_save.pack(padx=10, pady=2, ipady=5, fill=X)

        self.frame_export_forms = tk.Frame(self.frame_save, borderwidth=1, highlightthickness=0,
                                           highlightbackground="green")
        self.frame_export_forms.pack(fill=X)
        self.frame_save_file_name = tk.Frame(self.frame_save, borderwidth=1, highlightthickness=0,
                                             highlightbackground="black")
        self.frame_save_file_name.pack(fill=X)
        self.frame_export_type = tk.Frame(self.frame_save_file_name, borderwidth=1, highlightthickness=0,
                                          highlightbackground="yellow")
        self.frame_export_type.pack(side=RIGHT, padx=20)
        self.frame_save_folder = tk.Frame(self.frame_export_forms, borderwidth=1, highlightthickness=0,
                                          highlightbackground="red")
        self.frame_save_folder.pack(side=LEFT, pady=5, fill=X)

        self.frame_export_data_btn = tk.Frame(self.frame_save, borderwidth=1, highlightthickness=0,
                                              highlightbackground="orange")
        self.frame_export_data_btn.pack()

        self.frame_save_file = tk.Frame(self.frame_export_forms, borderwidth=1, highlightthickness=0,
                                        highlightbackground="blue")
        self.frame_save_file.pack(fill=X)

        self.save_browse_button = tk.Button(self.frame_save_folder, text="Select Output Folder",
                                            command=self.browsecsvexportfolder)
        self.save_browse_button.pack(side=LEFT, padx=5)
        self.label_exportpath_value = tk.Label(self.frame_save_folder, text="", width=128, anchor="w")
        self.label_exportpath_value.pack(side=LEFT)
        self.label_exportpath_value.configure(text=self.base_path + '\\Output')
        self.frame_folderpath = tk.Frame(self.frame_save)
        self.frame_folderpath.pack(side=LEFT)

        self.label_output_path = tk.Label(self.frame_save_file_name, text="File name:")
        self.label_output_path.pack(side=LEFT, padx=5)
        self.entry_output_path = tk.Entry(self.frame_save_file_name, width=60)
        self.entry_output_path.pack(side=LEFT)

        self.var_outputtype = tk.IntVar()
        self.var_outputtype.set(1)
        self.label_csv_type = tk.Label(self.frame_export_type, text="Output File Format:").pack(side=LEFT, padx=10)
        self.radio_outputtype = tk.Radiobutton(self.frame_export_type, text="CSV", padx=20,
                                               variable=self.var_outputtype,
                                               value=1).pack(side=LEFT)
        self.radio_outputtype = tk.Radiobutton(self.frame_export_type, text="Excel", padx=20,
                                               variable=self.var_outputtype,
                                               value=2).pack(side=LEFT)
        self.radio_outputtype = tk.Radiobutton(self.frame_export_type, text="JSON", padx=20,
                                               variable=self.var_outputtype,
                                               value=3).pack(side=LEFT)

        self.entry_output_path.insert(0, self.get_op_filename())

        self.save_file_button = tk.Button(self.frame_export_data_btn, text="EXPORT", height=1, width=25,
                                          command=self.csvfileexport)
        self.save_file_button.pack(side=LEFT, padx=5, ipadx=5, ipady=2, pady=5)
        self.open_folder_button = tk.Button(self.frame_export_data_btn, text="Open Output Folder", height=1, width=25,
                                            command=self.openfolderlocation)
        self.open_folder_button.pack(side=LEFT, padx=10, ipadx=5, ipady=2, pady=5)
        # -----------End of UI code---------------------------------------------------------------------

    def showinputinfo(self):
        messagebox.showinfo("Load Data - Information", "Info_Msg_Content_1")

    def browsefunc(self):
        ip_filenames = filedialog.askopenfilenames(defaultextension='.csv',
                                                   filetypes=[('CSV file', '*.csv'), ('CSV file', '*.CSV'),
                                                              ('All files', '*.*')])
        for items in ip_filenames:
            self.listbox_files.insert(END, items)
        self.autoloadheaders()

    def deleteFromItems(self):
        if (len(self.listbox_files.curselection()) > 0):
            self.listbox_files.delete(self.listbox_files.curselection())
        else:
            messagebox.showwarning("No File Selected", "Please select a file from  the list.")

    def deleteAllFromItems(self):
        self.listbox_files.delete(0, END)
        self.text_columnlist.configure(state='normal')
        self.text_columnlist.delete('1.0', END)
        self.text_columnlist.configure(state='disabled')

    def loadheaders(self):
        self.text_columnlist.configure(state='normal')
        if (len(self.listbox_files.curselection()) > 0):
            try:
                filetoloadheader = self.listbox_files.get(ACTIVE)
                with open(filetoloadheader) as f:
                    first_line = f.readline().split(self.DELIMITER)
                self.text_columnlist.delete('1.0', END)
                first_ex = True
                for col in first_line:
                    if first_ex == True:
                        self.text_columnlist.insert(END, col)
                        first_ex = False
                    else:
                        self.text_columnlist.insert(END, ',')
                        self.text_columnlist.insert(END, col)
                self.text_columnlist.configure(state='disabled')
            except Exception as err:
                messagebox.showerror("Error", str(err))
        else:
            messagebox.showwarning("No File Selected", "Please select a file from  the list.")

    def autoloadheaders(self):
        self.text_columnlist.configure(state='normal')
        if (self.listbox_files.size() > 0):
            try:
                if (len(self.listbox_files.curselection()) > 0):
                    filetoloadheader = self.listbox_files.get(ACTIVE)
                else:
                    filetoloadheader = self.listbox_files.get(0)
                with open(filetoloadheader) as f:
                    first_line = f.readline().split(self.DELIMITER)
                self.text_columnlist.delete('1.0', END)
                # listbox_available_headers.delete(0,END)
                first_ex = True
                for col in first_line:
                    # listbox_available_headers.insert(END,col)
                    if first_ex == True:
                        self.text_columnlist.insert(END, col)
                        first_ex = False
                    else:
                        self.text_columnlist.insert(END, ',')
                        self.text_columnlist.insert(END, col)
                self.text_columnlist.configure(state='disabled')
            except Exception as err:
                messagebox.showerror("Error", str(err))

    def loadFiles(self):
        inputype = self.var_inputtype.get()
        if (self.listbox_files.size() > 0):
            if inputype == 1:
                self.combineFilesWithSameHeaders()
            else:
                self.combineFilesWithDifferentHeaders()
            if self.dframe.empty:
                messagebox.showerror("Data Frame Empty",
                                     "The data frame is empty. Please select valid CSV file(s) and load it using the Load Data button.")
            else:
                try:
                    if self.var_dropemptycolumns.get() == 1:
                        self.dframe.dropna(how='all', axis=1, inplace=True)  # drop empty columns
                    if self.var_dropblankrows.get() == 1:
                        self.dframe.dropna(subset=self.dframe.columns[0:], how='all',
                                           inplace=True)  # removes blank rows
                    if self.var_dropblankrowswithcolum1data.get() == 1:
                        self.dframe.dropna(subset=self.dframe.columns[1:], how='all',
                                           inplace=True)  # removes  rows with blank from col 2
                    if self.var_dropduplicatelines.get() == 1:
                        self.dframe.drop_duplicates(subset=None,
                                                    inplace=True)  # removes duplicates. Notes:the `subset=None` means that every column is used

                    if self.var_fill_nan_onload.get() == 1:
                        if self.var_fill_nan_method.get() == 1:
                            # self.dframe.fillna(self.dframe.mean(), inplace=True)
                            self.dframe.fillna(self.dframe.mean(numeric_only=True), inplace=True)
                        elif self.var_fill_nan_method.get() == 2:
                            self.dframe.fillna(self.dframe.median(), inplace=True)
                        elif self.var_fill_nan_method.get() == 3:
                            self.dframe.fillna(self.dframe.mode(), inplace=True)
                        elif self.var_fill_nan_method.get() == 4:
                            self.dframe.fillna(0, inplace=True)
                        elif self.var_fill_nan_method.get() == 5:
                            self.dframe.dropna(inplace=True)

                    self.sync_dframe()
                except Exception as err:
                    messagebox.showerror("Unable to clean the file",
                                         "Unable to clean the file due to error:" + str(err) + ". Please try again.")
            if self.dframe.empty:
                self.label_df_status.configure(text="DATA FRAME EMPTY", fg="blue")
        else:
            messagebox.showerror("Empty File List", "File list is empty. Please add atleast one file to the list.")

    def sync_dframe(self):
        helper_object_dp.set_dframe(self.dframe)

    def combineFilesWithSameHeaders(self):  # load data function
        ignorewarning = self.var_ignore_loadwarning.get()
        headercount = 0
        firsttime = True
        list_ = []
        self.autoloadheaders()
        ok_to_load = True
        self.listbox_available_headers.delete(0, END)
        self.listbox_outlierlist_headers.delete(0, END)
        try:
            for filename in self.listbox_files.get(0, END):
                if ignorewarning == 0:
                    with open(filename) as f:
                        headercount = len(f.readline().split(self.DELIMITER))
                    if firsttime:
                        first_headercount = headercount
                        firsttime = False
                    if first_headercount != headercount:
                        ok_to_load = False
                        messagebox.showwarning("Header Count Mismatch",
                                               "The number of columns in the input files are not same. Please combine the files that have similar columns.")
                else:
                    ok_to_load = True
                if ignorewarning == 0:
                    df = pd.read_csv(filename, index_col=None, header=0)  # # error_bad_lines=False
                else:
                    df = pd.read_csv(filename, index_col=None, header=0, error_bad_lines=False)
                list_.append(df)
            if ok_to_load:
                self.dframe = pd.concat(list_, axis=0, ignore_index=True)  # add 'sort=False' for some versions
                for h in self.dframe.columns:
                    self.listbox_available_headers.insert(END, h)
                self.label_df_status.configure(text="DATA LOADED", fg="green")
                helper_object_dp.label_footer_df_status.configure(
                    text=f"DATA LOADED   ( {str(self.dframe.shape[1])} columns x {str(self.dframe.shape[0])} rows )")
                if self.dframe.empty:
                    self.label_df_status.configure(text="EMPTY")
                    helper_object_dp.label_footer_df_status.configure(text="EMPTY")
            # print(dframe)
        except Exception as err:
            errortype = str(err).split('.')[0].strip()
            errordetails = str(err)
            if errortype == 'Error tokenizing data':
                messagebox.showerror("Error",
                                     "Rows found in data with no corresponding column header." + errordetails + ". \n\nPlease load data again with 'Ignore data errors' checkbox enabled to skip the bad rows. Or remove the bad rows or columns in the data manually before loading to prevent skipping bad rows.")
            else:
                messagebox.showerror("Error", str(err))

    def combineFilesWithDifferentHeaders(self):  # load data with different headers
        ignorewarning = self.var_ignore_loadwarning.get()
        rowcount = 0
        firsttime = True
        list_ = []
        self.autoloadheaders()
        ok_to_load = True
        self.listbox_available_headers.delete(0, END)
        self.listbox_outlierlist_headers.delete(0, END)
        try:
            for filename in self.listbox_files.get(0, END):
                if ignorewarning == 0:
                    df = pd.read_csv(filename, index_col=None, header=0)
                    rowcount = len(df)
                    if firsttime:
                        first_rowcount = rowcount
                        firsttime = False
                    if first_rowcount != rowcount:
                        ok_to_load = False
                        messagebox.showwarning("Mismatch in the number of rows",
                                               "The number of rows in the input files are not same. Please combine the files that have similar number of rows.")
                else:
                    df = pd.read_csv(filename, index_col=None, header=0, error_bad_lines=False)
                    ok_to_load = True
                list_.append(df)
            if ok_to_load:
                self.dframe = pd.concat(list_, axis=1)
                for h in self.dframe.columns:
                    self.listbox_available_headers.insert(END, h)
                self.label_df_status.configure(text="DATA LOADED", fg="green")
                helper_object_dp.label_footer_df_status.configure(
                    text=f"DATA LOADED   ( {str(self.dframe.shape[1])} columns x {str(self.dframe.shape[0])} rows )")
                if self.dframe.empty:
                    self.label_df_status.configure(text="EMPTY")
                    helper_object_dp.label_footer_df_status.configure(text="EMPTY")
            # print(dframe)
        except Exception as err:
            errortype = str(err).split('.')[0].strip()
            errordetails = str(err)
            if errortype == 'Error tokenizing data':
                messagebox.showerror("Error",
                                     "Rows found in data with no corresponding column header." + errordetails + ". \n\nPlease load data again with 'Ignore data errors' checkbox enabled to skip the bad rows. Or remove the bad rows or columns in the data manually before loading to prevent skipping bad rows.")
            else:
                messagebox.showerror("Error", str(err))

    def showinputinfo(self):
        messagebox.showinfo("Load Data - Information", configurable_constants.Info_Msg_Content_1)

    def showoutlierremovalinfo(self):
        messagebox.showinfo("Outlier Removal - Information", configurable_constants.Info_Msg_Content_2)

    # -------------Outlier Removal------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def removeColumns(self):
        if self.dframe.empty:
            messagebox.showerror("Data Frame Empty",
                                 "The data frame is empty. Please select CSV file(s) and load it using the Load Data button.")
        else:
            if (self.listbox_outlierlist_headers.size() > 0):
                df2 = self.dframe.drop(self.outlier_column_list, axis=1)
                self.dframe = df2
                self.listbox_available_headers.delete(0, END)
                self.listbox_outlierlist_headers.delete(0, END)
                for col in self.dframe.columns:
                    self.listbox_available_headers.insert(END, col)
                messagebox.showinfo("Columns Removed", "Selected columns removed from the data.")
                self.outlier_column_list = []
            else:
                messagebox.showwarning("Outlier Removal",
                                       "No columns selected for removing outliers. Please add columns for outlier removal.")

        self.sync_dframe()

    def get_1_5_IQR(self, df, column):  # method 1:   1.5IQR Rule
        # Computing IQR
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        # Filtering Values between Q1-1.5IQR and Q3+1.5IQR
        qry = '(@Q1 - 1.5 * @IQR) <= ' + column + ' <= (@Q3 + 1.5 * @IQR)'
        filtered = df.query(qry)
        return filtered

    def removeOutliers(self):
        if self.dframe.empty:
            messagebox.showerror("Data Frame Empty",
                                 "The data frame is empty. Please select CSV file(s) and load it using the Load Data button.")
        else:
            if (self.listbox_outlierlist_headers.size() > 0):
                for col in self.outlier_column_list:
                    self.dframe = self.get_1_5_IQR(self.dframe, col)
                messagebox.showinfo("Outlier Removal",
                                    "Outliers removed in the selected columns based on 1.5 IQR method.")
            else:
                messagebox.showwarning("Outlier Removal",
                                       "No columns selected for removing outliers. Please add columns for outlier removal.")
        self.sync_dframe()

    def addtoOutlierList(self):
        if (len(self.listbox_available_headers.curselection()) > 0):
            currentitem = self.listbox_available_headers.get(ACTIVE)
            if not currentitem in self.outlier_column_list:
                self.outlier_column_list.append(currentitem)
                self.listbox_outlierlist_headers.insert(END, currentitem)
        else:
            messagebox.showwarning("No columns selected", "No columns selected for adding to list.")

    def addalltoOutlierList(self):
        if self.dframe.empty:
            messagebox.showwarning("Data Frame Empty",
                                   "The data frame is empty. Please select CSV file(s) and load it using the Load Data button.")
        else:
            for item in self.listbox_available_headers.get(0, END):
                if not item in self.outlier_column_list:
                    self.outlier_column_list.append(item)
                    self.listbox_outlierlist_headers.insert(END, item)

    def removefromOutlierList(self):
        if (len(self.listbox_outlierlist_headers.curselection()) > 0):
            currentremitem = self.listbox_outlierlist_headers.get(ACTIVE)
            if currentremitem in self.outlier_column_list:
                self.outlier_column_list.remove(currentremitem)
            self.listbox_outlierlist_headers.delete(self.listbox_outlierlist_headers.curselection())
        else:
            messagebox.showwarning("No columns selected", "No columns selected for removing to list.")

    def removeallfromOutlierList(self):
        self.outlier_column_list.clear()
        self.listbox_outlierlist_headers.delete(0, END)

    # -------------CSV Export----------------------------------------------------------------------------------------------------------------------------------------------
    def get_op_filename(self):
        try:
            ts = time.time()
            dtt = datetime.datetime.fromtimestamp(ts).strftime('%d%m%Y_%H%M%S')
            op_filename = "Data_" + str(dtt)
        except Exception as err:
            print("Fun:get_op_filename() -", err)
        return op_filename

    def browsecsvexportfolder(self):
        output_path = filedialog.askdirectory()
        if not output_path == "":
            self.label_exportpath_value.configure(text=output_path)

    def csvfileexport(self):
        if self.dframe.empty:
            messagebox.showerror("Data Frame Empty",
                                 "The data frame is empty. Please select CSV file(s) and load it using the Load Data button.")
        else:
            exportfilename = os.path.join(self.label_exportpath_value.cget("text"), self.entry_output_path.get())
            if exportfilename == "":
                messagebox.showerror("Invlid Output Path", "Please enter a valid output path")
            else:
                try:
                    helper_object_dp.ensure_dir(exportfilename)
                    outputype = self.var_outputtype.get()
                    if outputype == 2:
                        exportfilename = os.path.join(self.label_exportpath_value.cget("text"),
                                                      self.entry_output_path.get() + '.xlsx')
                        self.dframe.to_excel(exportfilename, index=False)
                    elif outputype == 3:
                        exportfilename = os.path.join(self.label_exportpath_value.cget("text"),
                                                      self.entry_output_path.get() + '.json')
                        self.dframe.to_json(exportfilename)
                    else:
                        exportfilename = os.path.join(self.label_exportpath_value.cget("text"),
                                                      self.entry_output_path.get() + '.csv')
                        self.dframe.to_csv(exportfilename, index=False)
                    messagebox.showinfo("Export Data", "Data exported to: " + exportfilename)
                except Exception as err:
                    print('Error:', err)

    def openfolderlocation(self):
        op_folder = self.label_exportpath_value.cget("text")
        if not os.path.exists(op_folder):
            os.makedirs(op_folder)
        win_dir = os.path.normpath(op_folder)
        subprocess.Popen('explorer "%s"' % win_dir)

    # -------------------------------------------
    def view_data_summary(self, Transpose=False):
        try:
            if self.dframe.empty:
                messagebox.showwarning("Data Not Loaded", "Please note that there is no data loaded.")
            else:
                data_summary_top = tk.Toplevel()
                data_summary_top.title('Data Summary')
                data_summary_top.geometry("1000x600")
                # data_summary_top.attributes('-topmost', True)
                txt_widget = Text(data_summary_top)
                df_describe_table = tabulate(
                    self.dframe.describe().transpose() if Transpose else self.dframe.describe(), headers='keys',
                    tablefmt='pretty')
                txt_widget.insert(INSERT, df_describe_table)  # Inserting table in text widget
                txt_widget.pack(expand=True, fill=BOTH)
        except Exception as err:
            messagebox.showerror("Data Not Loaded", "Please note that there is no data loaded.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def view_data_head(self, rows: int = 5):
        try:
            if self.dframe.empty:
                messagebox.showwarning("Data Not Loaded", "Please note that there is no data loaded.")
            else:
                data_head_top = tk.Toplevel()
                data_head_top.title('Data Sample')
                data_head_top.geometry("1000x600")
                # data_summary_top.attributes('-topmost', True)
                txt_widget = Text(data_head_top)
                df_head_table = tabulate(self.dframe.head(rows), headers='keys', tablefmt='pretty')
                txt_widget.insert(INSERT, df_head_table)
                txt_widget.pack(expand=True, fill=BOTH)
        except Exception as err:
            messagebox.showerror("Data Not Loaded", "An error occured while processing the request.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def view_data_types(self):
        try:
            if self.dframe.empty:
                messagebox.showwarning("Data Not Loaded", "Please note that there is no data loaded.")
            else:
                data_head_top = tk.Toplevel()
                data_head_top.title('Data Types')
                data_head_top.geometry("400x500")
                txt_widget = Text(data_head_top)
                df_types_table = tabulate(self.dframe.dtypes.to_frame(), headers=('Column', 'Data type'),
                                          tablefmt='pretty')
                txt_widget.insert(INSERT, df_types_table)
                txt_widget.pack(expand=True, fill=BOTH)
        except Exception as err:
            messagebox.showerror("Data Not Loaded", "An error occured while processing the request.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def view_data_info(self):
        try:
            if self.dframe.empty:
                messagebox.showwarning("Data Not Loaded", "Please note that there is no data loaded.")
            else:
                data_head_top = tk.Toplevel()
                data_head_top.title('Data Info')
                data_head_top.geometry("600x600")
                txt_widget = Text(data_head_top)
                buffer = io.StringIO()
                self.dframe.info(buf=buffer)
                string_data = buffer.getvalue()
                txt_widget.insert(INSERT, string_data)
                txt_widget.pack(expand=True, fill=BOTH)
        except Exception as err:
            messagebox.showerror("Data Not Loaded", "An error occured while processing the request.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def enable_impute_options_onload(self):
        """Function for making impute options inactive in case box is not checked"""
        if self.var_fill_nan_onload.get() == 0:
            self.radio_fill_nan_method1.configure(state=DISABLED)
            self.radio_fill_nan_method2.configure(state=DISABLED)
            self.radio_fill_nan_method3.configure(state=DISABLED)
            self.radio_fill_nan_method4.configure(state=DISABLED)
            self.radio_fill_nan_method5.configure(state=DISABLED)
        else:
            self.radio_fill_nan_method1.configure(state=NORMAL)
            self.radio_fill_nan_method2.configure(state=NORMAL)
            self.radio_fill_nan_method3.configure(state=NORMAL)
            self.radio_fill_nan_method4.configure(state=NORMAL)
            self.radio_fill_nan_method5.configure(state=NORMAL)

    def impute_selcted_columns(self):
        if self.dframe.empty:
            messagebox.showerror("Data Frame Empty",
                                 "The data frame is empty. Please select CSV file(s) and load it using the Load Data button.")
        else:
            if (self.listbox_outlierlist_headers.size() > 0):
                if self.var_impute_method.get() == 1:
                    self.dframe[self.outlier_column_list] = self.dframe[self.outlier_column_list].fillna(
                        (self.dframe[self.outlier_column_list].mean()))
                elif self.var_impute_method.get() == 2:
                    self.dframe[self.outlier_column_list] = self.dframe[self.outlier_column_list].fillna(
                        (self.dframe[self.outlier_column_list].median()))
                elif self.var_impute_method.get() == 3:
                    self.dframe[self.outlier_column_list] = self.dframe[self.outlier_column_list].fillna(
                        (self.dframe[self.outlier_column_list].mode()))
                messagebox.showinfo("Successful", "Imputation done for the selected columns.")
            else:
                messagebox.showwarning("Unsuccessful",
                                       "No columns selected for the operation.")

        self.sync_dframe()

    def onehot_encode_category_DP(self):
        if self.dframe.empty:
            messagebox.showerror("Data Frame Empty",
                                 "The data frame is empty. Please select CSV file(s) and load it using the Load Data button.")
        else:
            if (self.listbox_outlierlist_headers.size() > 0):
                for col in self.outlier_column_list:
                    self.dframe[col] = self.dframe[col].astype('category')

                categorical_columns = list(set(self.outlier_column_list).intersection(
                    self.dframe.select_dtypes(include=['object', 'category']).columns.tolist()))
                if categorical_columns:
                    one_hot = pd.get_dummies(self.dframe[categorical_columns])
                    # Drop columns as it is now encoded
                    self.dframe = self.dframe.drop(categorical_columns, axis=1)
                    # Join the encoded df
                    self.dframe = self.dframe.join(one_hot)

                    self.listbox_available_headers.delete(0, END)
                    self.listbox_outlierlist_headers.delete(0, END)
                    for col in self.dframe.columns:
                        self.listbox_available_headers.insert(END, col)
                    for column in categorical_columns:
                        if column in self.outlier_column_list:
                            self.outlier_column_list.remove(column)

                self.sync_dframe()
                messagebox.showinfo("Success",
                                    f"The selected columns have been onehot encoded. Please note that the original columns were removed.")
            else:
                messagebox.showwarning("Warning",
                                       "No columns selected for the operation.")
