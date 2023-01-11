# -------------------------------------------------------------------------------
# Name:        ml_predict.py
# Purpose:     ML predictions
# Project:     dsmltool - BITS M.Tech Dissertation
# Author:      Abit K Sebin
#
# Created:     Jun - Aug 2022
# Copyright:   (c) abitk 2022
# Licence:     <None>
# -------------------------------------------------------------------------------
import json
import pickle
import sys
import tkinter as tk
from tkinter import X, LEFT, W, filedialog, messagebox

import pandas as pd

import configurable_constants
from common_functions_helper import Helper

log = Helper.getInstance().get_logger()
helper_object_ml_pred = Helper.getInstance()


class MlPrediction:
    """Class that has all UI components and variables for ML Prediction Tab """

    def __init__(self, tab_ml_predict):
        self.tab_ml_predict = tab_ml_predict
        self.model_MLPRED_CLS = None
        self.input_model_file_MLPRED_CLS = None
        self.input_data_file_MLPRED_CLS = None
        self.output_data_file_name_MLPRED_CLS = None
        self.label_info_MLPRED = tk.Label(self.tab_ml_predict, font='Helvetica 8 italic',
                                          text="Machine Learning - Prediction.",
                                          anchor="w")
        self.label_info_MLPRED.pack(fill=X, pady=10, padx=20)
        # -------classification--------
        self.labelframe_MLPRED_CLS = tk.LabelFrame(self.tab_ml_predict, text="Classification")
        self.labelframe_MLPRED_CLS.pack(padx=10, pady=5, ipady=2, fill=X)

        self.frame_MLPRED_CLS_row1 = tk.Frame(self.labelframe_MLPRED_CLS, borderwidth=0, highlightthickness=0,
                                              highlightbackground="green")
        self.frame_MLPRED_CLS_row1.pack(fill=X, ipady=2, padx=5)

        self.frame_MLPRED_CLS_row1_status = tk.Frame(self.frame_MLPRED_CLS_row1, borderwidth=0, highlightthickness=0,
                                                     highlightbackground="green")
        self.frame_MLPRED_CLS_row1_status.pack(fill=X, ipady=2, padx=5)
        tk.Label(self.frame_MLPRED_CLS_row1_status, text="Model Status:", anchor=W).pack(side=LEFT)

        self.label_MLPRED_CLS_model_status = tk.Label(self.frame_MLPRED_CLS_row1_status, text="No model loaded",
                                                      anchor=W)
        self.label_MLPRED_CLS_model_status.pack(side=LEFT)

        self.frame_MLPRED_CLS_row1_select_model = tk.Frame(self.frame_MLPRED_CLS_row1, borderwidth=0,
                                                           highlightthickness=0,
                                                           highlightbackground="blue")
        self.frame_MLPRED_CLS_row1_select_model.pack(pady=5, anchor=W, )

        self.button_MLPRED_CLS_select_model = tk.Button(self.frame_MLPRED_CLS_row1_select_model, text="Select Model",
                                                        height=1, width=24,
                                                        command=self.select_MLPRED_CLS_model)
        self.button_MLPRED_CLS_select_model.pack(side=LEFT)

        self.label_MLPRED_CLS_model_selected = tk.Label(self.frame_MLPRED_CLS_row1_select_model,
                                                        text="No model selected.", width=100, anchor=W)
        self.label_MLPRED_CLS_model_selected.pack(side=LEFT)
        self.frame_MLPRED_CLS_row1_select_data = tk.Frame(self.frame_MLPRED_CLS_row1, borderwidth=0,
                                                          highlightthickness=0,
                                                          highlightbackground="blue")
        self.frame_MLPRED_CLS_row1_select_data.pack(anchor=W, pady=5)

        self.button_MLPRED_CLS_select_data = tk.Button(self.frame_MLPRED_CLS_row1_select_data,
                                                       text="Select Data for Prediction",
                                                       height=1, width=24,
                                                       command=self.select_MLPRED_CLS_data)
        self.button_MLPRED_CLS_select_data.pack(side=LEFT)

        self.label_MLPRED_CLS_data_selected = tk.Label(self.frame_MLPRED_CLS_row1_select_data,
                                                       text="No input data is selected for prediction.", width=100,
                                                       anchor=W)
        self.label_MLPRED_CLS_data_selected.pack(side=LEFT, anchor=W)
        self.frame_MLPRED_CLS_row1_select_lemap_file = tk.Frame(self.frame_MLPRED_CLS_row1, borderwidth=0,
                                                                highlightthickness=0,
                                                                highlightbackground="blue")
        self.frame_MLPRED_CLS_row1_select_lemap_file.pack(anchor=W, pady=3)

        self.button_MLPRED_CLS_row1_select_lemap_file = tk.Button(self.frame_MLPRED_CLS_row1_select_lemap_file,
                                                                  text="Select Label Encode Mapping",
                                                                  height=1, width=24,
                                                                  command=self.select_MLPRED_CLS_lemap_file)
        self.button_MLPRED_CLS_row1_select_lemap_file.pack(side=LEFT)

        self.label_MLPRED_CLS_row1_select_lemap_file = tk.Label(self.frame_MLPRED_CLS_row1_select_lemap_file,
                                                                text="No label encode mapping file selected. (Optional - Load it to get label names in the prediction)",
                                                                width=100, anchor=W)
        self.label_MLPRED_CLS_row1_select_lemap_file.pack(side=LEFT, anchor=W)
        self.frame_MLPRED_CLS_row1_select_output_file = tk.Frame(self.frame_MLPRED_CLS_row1, borderwidth=0,
                                                                 highlightthickness=0,
                                                                 highlightbackground="blue")
        self.frame_MLPRED_CLS_row1_select_output_file.pack(anchor=W, pady=3)

        self.button_MLPRED_CLS_row1_select_output_file = tk.Button(self.frame_MLPRED_CLS_row1_select_output_file,
                                                                   text="Select Output Path",
                                                                   height=1, width=24,
                                                                   command=self.select_MLPRED_CLS_output_file)
        self.button_MLPRED_CLS_row1_select_output_file.pack(side=LEFT)

        self.label_MLPRED_CLS_row1_select_output_file = tk.Label(self.frame_MLPRED_CLS_row1_select_output_file,
                                                                 text="No output file is selected for prediction.",
                                                                 width=100, anchor=W)
        self.label_MLPRED_CLS_row1_select_output_file.pack(side=LEFT, anchor=W)

        self.button_MLPRED_CLS_execute = tk.Button(self.frame_MLPRED_CLS_row1,
                                                   text="Predict and Export",
                                                   height=2, width=25,
                                                   command=self.run_MLPRED_CLS)
        self.button_MLPRED_CLS_execute.pack(pady=6)
        self.var_MLPRED_CLS_lemap_file_name = None
        self.var_MLPRED_CLS_lemap = None
        # --------Regression
        self.labelframe_MLPRED_REG = tk.LabelFrame(self.tab_ml_predict, text="Regression")
        self.labelframe_MLPRED_REG.pack(padx=10, pady=20, ipady=2, fill=X)

        self.frame_MLPRED_REG_row1 = tk.Frame(self.labelframe_MLPRED_REG, borderwidth=0, highlightthickness=0,
                                              highlightbackground="green")
        self.frame_MLPRED_REG_row1.pack(fill=X, ipady=2, padx=5)

        self.frame_MLPRED_REG_row1_status = tk.Frame(self.frame_MLPRED_REG_row1, borderwidth=0, highlightthickness=0,
                                                     highlightbackground="green")
        self.frame_MLPRED_REG_row1_status.pack(fill=X, ipady=2, padx=5)
        tk.Label(self.frame_MLPRED_REG_row1_status, text="Model Status:", anchor=W).pack(side=LEFT)

        self.label_MLPRED_REG_model_status = tk.Label(self.frame_MLPRED_REG_row1_status, text="No model loaded",
                                                      anchor=W)
        self.label_MLPRED_REG_model_status.pack(side=LEFT)

        self.frame_MLPRED_REG_row1_select_model = tk.Frame(self.frame_MLPRED_REG_row1, borderwidth=0,
                                                           highlightthickness=0,
                                                           highlightbackground="blue")
        self.frame_MLPRED_REG_row1_select_model.pack(pady=5, anchor=W, )

        self.button_MLPRED_REG_select_model = tk.Button(self.frame_MLPRED_REG_row1_select_model, text="Select Model",
                                                        height=1, width=24,
                                                        command=self.select_MLPRED_REG_model)
        self.button_MLPRED_REG_select_model.pack(side=LEFT)

        self.label_MLPRED_REG_model_selected = tk.Label(self.frame_MLPRED_REG_row1_select_model,
                                                        text="No model selected.", width=100, anchor=W)
        self.label_MLPRED_REG_model_selected.pack(side=LEFT)
        self.frame_MLPRED_REG_row1_select_data = tk.Frame(self.frame_MLPRED_REG_row1, borderwidth=0,
                                                          highlightthickness=0,
                                                          highlightbackground="blue")
        self.frame_MLPRED_REG_row1_select_data.pack(anchor=W, pady=5)

        self.button_MLPRED_REG_select_data = tk.Button(self.frame_MLPRED_REG_row1_select_data,
                                                       text="Select Data for Prediction",
                                                       height=1, width=24,
                                                       command=self.select_MLPRED_REG_data)
        self.button_MLPRED_REG_select_data.pack(side=LEFT)

        self.label_MLPRED_REG_data_selected = tk.Label(self.frame_MLPRED_REG_row1_select_data,
                                                       text="No input data is selected for prediction.", width=100,
                                                       anchor=W)
        self.label_MLPRED_REG_data_selected.pack(side=LEFT, anchor=W)

        self.frame_MLPRED_REG_row1_select_output_file = tk.Frame(self.frame_MLPRED_REG_row1, borderwidth=0,
                                                                 highlightthickness=0,
                                                                 highlightbackground="blue")
        self.frame_MLPRED_REG_row1_select_output_file.pack(anchor=W, pady=3)

        self.button_MLPRED_REG_row1_select_output_file = tk.Button(self.frame_MLPRED_REG_row1_select_output_file,
                                                                   text="Select Output Path",
                                                                   height=1, width=24,
                                                                   command=self.select_MLPRED_REG_output_file)
        self.button_MLPRED_REG_row1_select_output_file.pack(side=LEFT)

        self.label_MLPRED_REG_row1_select_output_file = tk.Label(self.frame_MLPRED_REG_row1_select_output_file,
                                                                 text="No output file is selected for prediction.",
                                                                 width=100, anchor=W)
        self.label_MLPRED_REG_row1_select_output_file.pack(side=LEFT, anchor=W)

        self.button_MLPRED_REG_execute = tk.Button(self.frame_MLPRED_REG_row1,
                                                   text="Predict and Export",
                                                   height=2, width=25,
                                                   command=self.run_MLPRED_REG)
        self.button_MLPRED_REG_execute.pack(pady=6)
        self.model_MLPRED_REG = None

    def select_MLPRED_CLS_model(self):
        try:
            ip_filename = filedialog.askopenfilenames(
                defaultextension=f'.{configurable_constants.MODEL_EXPORT_EXTENSION}',
                filetypes=[('DSMLTool Model', f'*.{configurable_constants.MODEL_EXPORT_EXTENSION}')])
            if ip_filename is None:
                return
            elif len(ip_filename) > 0:
                self.input_model_file_MLPRED_CLS = ip_filename[0]
                self.label_MLPRED_CLS_model_selected.configure(
                    text=f"{self.input_model_file_MLPRED_CLS}")
                self.model_MLPRED_CLS = pickle.load(open(self.input_model_file_MLPRED_CLS, 'rb'))
                self.label_MLPRED_CLS_model_status.configure(
                    text=f"{str(self.model_MLPRED_CLS)} - model imported from file.", fg="green")
        except Exception as err:
            messagebox.showerror("Error", "Unable to select model.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def select_MLPRED_CLS_data(self):
        try:
            ip_data_filename = filedialog.askopenfilenames(
                defaultextension='.csv', filetypes=[('CSV file', '*.csv'), ('CSV file', '*.CSV')])
            if ip_data_filename is None:
                return
            elif len(ip_data_filename) > 0:
                self.input_data_file_MLPRED_CLS = ip_data_filename[0]
                self.label_MLPRED_CLS_data_selected.configure(
                    text=f"{self.input_data_file_MLPRED_CLS}")
        except Exception as err:
            messagebox.showerror("Error", "Unable to select data.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def select_MLPRED_CLS_output_file(self):
        try:
            file_dialog = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
            if file_dialog is None:
                return
            self.output_data_file_name_MLPRED_CLS = file_dialog.name
            self.label_MLPRED_CLS_row1_select_output_file.configure(
                text=f"{self.output_data_file_name_MLPRED_CLS}")
        except Exception as err:
            messagebox.showerror("Error", "Unable to select output file.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def run_MLPRED_CLS(self):
        try:
            data_for_prediction = pd.read_csv(self.input_data_file_MLPRED_CLS)
            result = self.model_MLPRED_CLS.predict(data_for_prediction)
            data_for_prediction["Predicted"] = result
            if not self.var_MLPRED_CLS_lemap is None:
                data_for_prediction["Predicted_Labels"] = data_for_prediction["Predicted"].replace(
                    self.var_MLPRED_CLS_lemap)
            data_for_prediction.to_csv(self.output_data_file_name_MLPRED_CLS)
            messagebox.showinfo("Success", "Predicted data exported.")
            helper_object_ml_pred.update_bottom_status_bar("Predicted (classification) data exported.")
            #
        except Exception as err:
            messagebox.showerror("Error", f"Unable to run prediction.{str(err)}")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def select_MLPRED_CLS_lemap_file(self):
        try:
            lemap_filename_dialog = filedialog.askopenfilenames(
                defaultextension=f'.{configurable_constants.LABEL_ENCODE_EXPORT_EXTENSION}',
                filetypes=[('Label Encode Mapping', f'*.{configurable_constants.LABEL_ENCODE_EXPORT_EXTENSION}')])
            if lemap_filename_dialog is None:
                return
            elif len(lemap_filename_dialog) > 0:
                self.var_MLPRED_CLS_lemap_file_name = lemap_filename_dialog[0]
                self.label_MLPRED_CLS_row1_select_lemap_file.configure(
                    text=f"{self.var_MLPRED_CLS_lemap_file_name}")
                with open(self.var_MLPRED_CLS_lemap_file_name) as f:
                    le_map_content = f.read()
                    intermediate_data = json.loads(le_map_content)
                    self.var_MLPRED_CLS_lemap = {int(k): v for k, v in intermediate_data.items()}
                    print(self.var_MLPRED_CLS_lemap)
        except Exception as err:
            messagebox.showerror("Error", "Unable to select Label Encode Mapping.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def select_MLPRED_REG_model(self):
        try:
            ip_filename = filedialog.askopenfilenames(
                defaultextension=f'.{configurable_constants.MODEL_EXPORT_EXTENSION}',
                filetypes=[('DSMLTool Model', f'*.{configurable_constants.MODEL_EXPORT_EXTENSION}')])
            if ip_filename is None:
                return
            elif len(ip_filename) > 0:
                self.input_model_file_MLPRED_REG = ip_filename[0]
                self.label_MLPRED_REG_model_selected.configure(
                    text=f"{self.input_model_file_MLPRED_REG}")
                self.model_MLPRED_REG = pickle.load(open(self.input_model_file_MLPRED_REG, 'rb'))
                self.label_MLPRED_REG_model_status.configure(
                    text=f"{str(self.model_MLPRED_REG)} - model imported from file.", fg="green")
        except Exception as err:
            messagebox.showerror("Error", "Unable to select model.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def select_MLPRED_REG_data(self):
        try:
            ip_data_filename = filedialog.askopenfilenames(
                defaultextension='.csv', filetypes=[('CSV file', '*.csv'), ('CSV file', '*.CSV')])
            if ip_data_filename is None:
                return
            elif len(ip_data_filename) > 0:
                self.input_data_file_MLPRED_REG = ip_data_filename[0]
                self.label_MLPRED_REG_data_selected.configure(
                    text=f"{self.input_data_file_MLPRED_REG}")
        except Exception as err:
            messagebox.showerror("Error", "Unable to select data.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def select_MLPRED_REG_output_file(self):
        try:
            file_dialog = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
            if file_dialog is None:
                return
            self.output_data_file_name_MLPRED_REG = file_dialog.name
            self.label_MLPRED_REG_row1_select_output_file.configure(
                text=f"{self.output_data_file_name_MLPRED_REG}")
        except Exception as err:
            messagebox.showerror("Error", "Unable to select output file.")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def run_MLPRED_REG(self):
        try:
            data_for_prediction = pd.read_csv(self.input_data_file_MLPRED_REG)
            result = self.model_MLPRED_REG.predict(data_for_prediction)
            data_for_prediction["Predicted"] = result
            data_for_prediction.to_csv(self.output_data_file_name_MLPRED_REG)
            messagebox.showinfo("Success", "Predicted data exported.")
            helper_object_ml_pred.update_bottom_status_bar("Predicted (regression) data exported.")
        except Exception as err:
            messagebox.showerror("Error", f"Unable to run prediction.{str(err)}")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))
