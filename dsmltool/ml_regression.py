# -------------------------------------------------------------------------------
# Name:        ml_regression.py
# Purpose:     ML Regression Tab code of the tool
# Project:     dsmltool - BITS M.Tech Dissertation
# Author:      Abit K Sebin
#
# Created:     Jun - Aug 2022
# Copyright:   (c) abitk 2022
# Licence:     <None>
# -------------------------------------------------------------------------------
import pickle
import sys
import tkinter as tk
from datetime import datetime
from tkinter import END, LEFT, RIGHT, X, Y, ACTIVE, messagebox, filedialog, W, HORIZONTAL
from tkinter import ttk

from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import configurable_constants
from common_functions_helper import Helper


class MlRegressionAlgorithms:
    OLS = "OLS - Linear Regression"
    RIDGE = "Ridge Regression"
    LASSO = "Lasso"


log = Helper.getInstance().get_logger()
helper_object_ml_reg = Helper.getInstance()


class MlRegression:
    def __init__(self, tab_ml_regression):
        self.X = None
        self.tab_ml_regression = tab_ml_regression
        self.label_info_ml_clustering = tk.Label(self.tab_ml_regression, font='Helvetica 8 italic',
                                                 text="Machine Learning - Clustering.",
                                                 anchor="w")
        self.label_info_ml_clustering.pack(fill=X, pady=10, padx=20)

        self.frame_MLREG_row1 = tk.Frame(self.tab_ml_regression, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_MLREG_row1.pack(fill=X, padx=3)

        self.frame_MLREG_row1_available_columns = tk.Frame(self.frame_MLREG_row1, borderwidth=0, highlightthickness=0,
                                                           highlightbackground="yellow")
        self.frame_MLREG_row1_available_columns.pack(side=LEFT, pady=2)
        self.label_MLREG_available_headers = tk.Label(self.frame_MLREG_row1_available_columns, text="Filtered Columns")
        self.label_MLREG_available_headers.pack()
        self.scrollbar_MLREG_available_columns = tk.Scrollbar(self.frame_MLREG_row1_available_columns)
        self.scrollbar_MLREG_available_columns.pack(side=RIGHT, fill=Y)
        self.listbox_MLREG_available_columns = tk.Listbox(self.frame_MLREG_row1_available_columns, width=40, height=7,
                                                          yscrollcommand=self.scrollbar_MLREG_available_columns.set)
        self.listbox_MLREG_available_columns.pack()
        self.scrollbar_MLREG_available_columns.config(command=self.listbox_MLREG_available_columns.yview)

        self.frame_MLREG_row1_options_mid = tk.Frame(self.frame_MLREG_row1, borderwidth=0, highlightthickness=0,
                                                     highlightbackground="yellow")
        self.frame_MLREG_row1_options_mid.pack(side=LEFT, pady=2, padx=15, ipady=5)

        self.frame_MLREG_target_var = tk.Frame(self.frame_MLREG_row1_options_mid)
        self.frame_MLREG_target_var.pack(fill=X)
        tk.Label(self.frame_MLREG_target_var, text="Dependant Column:", font='Helvetica 9 bold').pack(side=LEFT)
        self.label_MLREG_target_var = tk.Label(self.frame_MLREG_target_var, text="Not Selected", font='arial 9 bold',
                                               width=20, anchor=W)
        self.label_MLREG_target_var.pack()

        self.button_MLREG_set_as_dependant = tk.Button(self.frame_MLREG_row1_options_mid,
                                                       text="Set column as as dependant", height=1, width=25,
                                                       command=self.add_MLREG_target)
        self.button_MLREG_set_as_dependant.pack(pady=3, padx=10, anchor=W)
        self.frame_MLREG_row1_options_algorithms = tk.Frame(self.frame_MLREG_row1_options_mid, borderwidth=0,
                                                            highlightthickness=0, highlightbackground="yellow")
        self.frame_MLREG_row1_options_algorithms.pack(pady=20, ipady=3)
        self.label_MLREG_algorithm = tk.Label(self.frame_MLREG_row1_options_algorithms, text="Algorithm:")
        self.label_MLREG_algorithm.pack(side=LEFT)

        self.var_MLREG_algorithm = tk.StringVar()
        self.combobox_MLREG_algorithm = ttk.Combobox(self.frame_MLREG_row1_options_algorithms,
                                                     textvariable=self.var_MLREG_algorithm,
                                                     values=[MlRegressionAlgorithms.OLS, MlRegressionAlgorithms.RIDGE,
                                                             MlRegressionAlgorithms.LASSO], state="readonly")
        self.combobox_MLREG_algorithm.current(1)
        self.combobox_MLREG_algorithm.pack(side=LEFT)
        self.selected_MLREG_target_column = helper_object_ml_reg.get_selected_target_column()

        self.frame_MLREG_row1_options_parent = tk.Frame(self.frame_MLREG_row1)
        self.frame_MLREG_row1_options_parent.pack(side=LEFT, pady=2, padx=20)

        self.frame_MLREG_row1_options = tk.LabelFrame(self.frame_MLREG_row1_options_parent, text="Options")
        self.frame_MLREG_row1_options.pack(pady=2, padx=20)
        self.regression_model = None
        self.var_MLREG_options_shuffle = tk.IntVar()
        self.var_MLREG_options_shuffle.set(1)
        self.checkbutton_MLREG_options_shuffle = tk.Checkbutton(self.frame_MLREG_row1_options, text="Shuffle data",
                                                                variable=self.var_MLREG_options_shuffle)
        self.checkbutton_MLREG_options_shuffle.pack(anchor=W, padx=5)
        self.frame_MLREG_row1_data_split_options = tk.Frame(self.frame_MLREG_row1)
        self.frame_MLREG_row1_data_split_options.pack(side=LEFT, pady=2, padx=20)

        self.frame_MLREG_row1_buttons_data_split = tk.LabelFrame(self.frame_MLREG_row1_data_split_options,
                                                                 text="Train -Test Split")
        self.frame_MLREG_row1_buttons_data_split.pack(ipadx=10, padx=5, ipady=5)

        # self.label_MLREG_train_test_split_heading = tk.Label(self.frame_MLREG_row1_buttons_slider_labels,text="Train-Test Split:").pack(side=LEFT)
        self.label_MLREG_train_test_split_data = tk.Label(self.frame_MLREG_row1_buttons_data_split,
                                                          text="Train:80%       Test:20%")
        self.label_MLREG_train_test_split_data.pack(pady=5)
        self.var_MLREG_train_test_input = tk.DoubleVar()
        self.slider_MLREG_train_test_split = tk.Scale(self.frame_MLREG_row1_buttons_data_split,
                                                      variable=self.var_MLREG_train_test_input,
                                                      from_=1, to=99, orient=HORIZONTAL,
                                                      command=self.update_traintest_split_slider, length=150,
                                                      showvalue=False)
        self.slider_MLREG_train_test_split.set(80)
        self.slider_MLREG_train_test_split.pack()

        self.frame_MLREG_train_test_split_rs = tk.Frame(self.frame_MLREG_row1_buttons_data_split)
        self.frame_MLREG_train_test_split_rs.pack(side=LEFT, pady=10)

        self.label_MLREG_train_test_split_rs = tk.Label(self.frame_MLREG_train_test_split_rs,
                                                        text="Random State:").pack(side=LEFT)
        self.var_MLREG_random_state = tk.IntVar()
        self.combobox_MLREG_random_state = ttk.Combobox(self.frame_MLREG_train_test_split_rs,
                                                        textvariable=self.var_MLREG_random_state,
                                                        values=[i for i in range(1000)], width=4)
        self.combobox_MLREG_random_state.current(42)
        self.combobox_MLREG_random_state.pack(side=LEFT)

        self.button_MLREG_train_model = tk.Button(self.frame_MLREG_row1_options_parent, text="Train Model",
                                                  command=self.start_MLREG_training, height=2, width=25)
        self.button_MLREG_train_model.pack(pady=10)

        self.frame_MLREG_row2 = tk.Frame(self.tab_ml_regression, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_MLREG_row2.pack(fill=X, padx=3)

        label_MLREG_train_test_split_heading = tk.Label(self.frame_MLREG_row2,
                                                        text="Results").pack()
        self.text_MLREG_train_results = tk.Text(self.frame_MLREG_row2, height=20, width=120)
        self.text_MLREG_train_results.pack(padx=3, pady=2)

        self.frame_MLREG_row3 = tk.Frame(self.tab_ml_regression, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_MLREG_row3.pack(fill=X, padx=10, pady=15, ipady=5)
        self.button_MLREG_export_model = tk.Button(self.frame_MLREG_row3, text="Export Model", height=2, width=20,
                                                   command=self.export_model)
        self.button_MLREG_export_model.pack(side=LEFT, padx=10, ipady=5)
        self.button_MLREG_export_predicted_data = tk.Button(self.frame_MLREG_row3, text="Export Final Data (X)",
                                                            height=2,
                                                            width=20, command=self.export_data_X)
        self.button_MLREG_export_predicted_data.pack(side=LEFT, padx=10, ipady=5)
        self.button_MLREG_export_model_to_pred = tk.Button(self.frame_MLREG_row3, text="Pass Model to Prediction Tab",
                                                           height=2,
                                                           width=24, command=self.export_model_to_pred)
        self.button_MLREG_export_model_to_pred.pack(side=LEFT, padx=10, ipady=5)

    def add_MLREG_target(self):
        if (len(self.listbox_MLREG_available_columns.curselection()) > 0):
            currentitem = self.listbox_MLREG_available_columns.get(ACTIVE)
            helper_object_ml_reg.set_selected_target_column(currentitem)
            self.selected_MLREG_target_column = currentitem
            self.label_MLREG_target_var.configure(text=self.selected_MLREG_target_column)
        else:
            messagebox.showerror("No items selected", "Please select a value from the list of available columns.")

    def update_traintest_split_slider(self, slider_value):
        self.label_MLREG_train_test_split_data.config(
            text=f"Train:{int(slider_value):02}%  Test:{100 - int(slider_value):02}%")

    def plot_MLREG_results(self):
        for column in self.X_test.columns:
            plt.scatter(self.X_test[column], self.y_test)
        plt.plot(self.X_test, self.model_prediction, color="blue", linewidth=3)
        plt.xticks(())
        plt.yticks(())
        plt.show()

    def start_MLREG_training(self):
        df = helper_object_ml_reg.get_dframe()
        dependant_column = helper_object_ml_reg.get_selected_target_column()
        selected_features = helper_object_ml_reg.get_selected_features_list()
        if df is None or len(selected_features) == 0 or dependant_column == None:
            messagebox.showerror("Error",
                                 "Please load data,confirm features and select dependant column before training.")
        else:
            try:
                """Function to do the  regression training"""
                helper_object_ml_reg.update_bottom_status_bar('Regression training requested.')
                self.text_MLREG_train_results.delete('1.0', END)

                if dependant_column in selected_features:
                    selected_features.remove(dependant_column)
                if self.var_MLREG_options_shuffle.get() == 1:
                    shuffle_required = True
                else:
                    shuffle_required = False
                self.X = df[selected_features]
                self.y = df[dependant_column]

                # train test split
                self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y,
                                                                                        shuffle=shuffle_required,
                                                                                        train_size=self.var_MLREG_train_test_input.get() / 100,
                                                                                        random_state=self.var_MLREG_random_state.get())

                if self.var_MLREG_algorithm.get() == MlRegressionAlgorithms.OLS:
                    self.regression_model = linear_model.LinearRegression()
                elif self.var_MLREG_algorithm.get() == MlRegressionAlgorithms.RIDGE:
                    self.regression_model = linear_model.Ridge(alpha=.5)
                elif self.var_MLREG_algorithm.get() == MlRegressionAlgorithms.LASSO:
                    self.regression_model = linear_model.Lasso(alpha=0.1)
                self.text_MLREG_train_results.insert(END,
                                                     f'>> Data splitted into Train-Test data in the ratio {self.var_MLREG_train_test_input.get()}:{100 - self.var_MLREG_train_test_input.get()}')
                # training model
                self.regression_model.fit(self.X_train, self.y_train)
                self.text_MLREG_train_results.insert(END,
                                                     f'\n>> Training started using the algorithm: {self.var_MLREG_algorithm.get()} at {str(datetime.now())}.')
                # predict
                self.model_prediction = self.regression_model.predict(self.X_test)
                self.text_MLREG_train_results.insert(END, f'\n>> Training completed at {str(datetime.now())}.\n')
                self.text_MLREG_train_results.insert(END, '\n>> Trained Model Summary:\n')
                self.text_MLREG_train_results.insert(END, '-' * 25)

                self.text_MLREG_train_results.insert(END,
                                                     f'\nCoefficients:\n {self.regression_model.coef_}')
                self.text_MLREG_train_results.insert(END,
                                                     f'\nMean squared error: {str(mean_squared_error(self.y_test, self.model_prediction))}')
                # The coefficient of determination: 1 is perfect prediction
                self.text_MLREG_train_results.insert(END,
                                                     f'\nCoefficient of determination: {str(r2_score(self.y_test, self.model_prediction))} \n')

                self.text_MLREG_train_results.insert(END, '--' * 50)
                helper_object_ml_reg.update_bottom_status_bar('Regression model training done.')
            except Exception as err:
                messagebox.showerror("Error", f"Unable do the requested action.{str(err)}")
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def export_model(self):
        if self.regression_model is None:
            messagebox.showerror("Model not trained", "The model is not trained. Please train before exporting.")
        else:
            try:
                file_dialog = filedialog.asksaveasfile(mode='w',
                                                       defaultextension=f".{configurable_constants.MODEL_EXPORT_EXTENSION}")
                if file_dialog is None:
                    return
                pickle.dump(self.regression_model, open(file_dialog.name, 'wb'))
                messagebox.showinfo("Exported", f"Model exported to the path : {file_dialog.name}")
            except Exception as err:
                messagebox.showerror("Error", "Unable to export model.")
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def export_data_X(self):
        if self.X is None:
            messagebox.showerror("Model not trained", "Please train before exporting.")
        else:
            try:
                file_dialog = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
                if file_dialog is None:
                    return
                self.X.to_csv(file_dialog.name)
                messagebox.showinfo("Exported", f"Data exported to the path : {file_dialog.name}")
            except Exception as err:
                messagebox.showerror("Error", f"Unable to export.{str(err)}")
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def export_model_to_pred(self):
        if self.regression_model is None:
            messagebox.showerror("Model not trained", "The model is not trained. Please train before exporting.")
        else:
            try:
                helper_object_ml_reg.get_ml_predict_obj().model_MLPRED_REG = self.regression_model

                helper_object_ml_reg.get_ml_predict_obj().label_MLPRED_REG_model_status.configure(
                    text=f"{helper_object_ml_reg.get_ml_predict_obj().model_MLPRED_REG} - Model imported from training "
                         f"tab.", fg="green")
                messagebox.showinfo("Exported", "Model pushed to prediction")
            except Exception as err:
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))
                messagebox.showerror("Error", f"Unable to export model.{str(err)}")
