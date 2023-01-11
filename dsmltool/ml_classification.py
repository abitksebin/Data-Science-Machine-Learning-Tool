# -------------------------------------------------------------------------------
# Name:        ml_classification.py
# Purpose:     ML Classification Tab code of the tool
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
from datetime import datetime
from tkinter import END, LEFT, RIGHT, X, Y, ACTIVE, messagebox, filedialog, W, HORIZONTAL
from tkinter import ttk

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

import configurable_constants
from common_functions_helper import Helper


class MlAlgorithms:
    SVM = "SVM"
    LOG_REGRESSION = "Logistic Regression"
    DECISION_TREE = "Decision Tree Classifier"


log = Helper.getInstance().get_logger()
helper_object_ml_cls = Helper.getInstance()


class MlClassification:
    """Class that has all UI components and variables for ML Training - Classification Tab """

    def __init__(self, tab_ml_classification):
        self.X = None
        self.tab_ml_classification = tab_ml_classification
        self.label_info_ml_classification = tk.Label(self.tab_ml_classification, font='Helvetica 8 italic',
                                                     text="Machine Learning - Classification.",
                                                     anchor="w")
        self.label_info_ml_classification.pack(fill=X, pady=10, padx=20)

        self.frame_MLCLS_row1 = tk.Frame(self.tab_ml_classification, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_MLCLS_row1.pack(fill=X, padx=3)

        self.frame_MLCLS_row1_available_columns = tk.Frame(self.frame_MLCLS_row1, borderwidth=0, highlightthickness=0,
                                                           highlightbackground="yellow")
        self.frame_MLCLS_row1_available_columns.pack(side=LEFT, pady=2)
        self.label_MLCLS_available_headers = tk.Label(self.frame_MLCLS_row1_available_columns, text="Filtered Columns")
        self.label_MLCLS_available_headers.pack()
        self.scrollbar_MLCLS_available_columns = tk.Scrollbar(self.frame_MLCLS_row1_available_columns)
        self.scrollbar_MLCLS_available_columns.pack(side=RIGHT, fill=Y)
        self.listbox_MLCLS_available_columns = tk.Listbox(self.frame_MLCLS_row1_available_columns, width=40, height=7,
                                                          yscrollcommand=self.scrollbar_MLCLS_available_columns.set)
        self.listbox_MLCLS_available_columns.pack()
        self.scrollbar_MLCLS_available_columns.config(command=self.listbox_MLCLS_available_columns.yview)

        self.frame_MLCLS_row1_options_mid = tk.Frame(self.frame_MLCLS_row1, borderwidth=0, highlightthickness=0,
                                                     highlightbackground="yellow")
        self.frame_MLCLS_row1_options_mid.pack(side=LEFT, pady=2, padx=15, ipady=5)

        self.frame_MLCLS_target_var = tk.Frame(self.frame_MLCLS_row1_options_mid)
        self.frame_MLCLS_target_var.pack(fill=X)
        tk.Label(self.frame_MLCLS_target_var, text="Target Column: ", font='Helvetica 9 bold').pack(side=LEFT)
        self.label_MLCLS_target_var = tk.Label(self.frame_MLCLS_target_var, text="Not Selected", font='arial 9 bold')
        self.label_MLCLS_target_var.pack(side=LEFT, anchor=W)

        self.button_MLCLS_addas_target = tk.Button(self.frame_MLCLS_row1_options_mid,
                                                   text="Set selected column as as target", height=1, width=25,
                                                   command=self.add_MLCLS_target)
        self.button_MLCLS_addas_target.pack(pady=3, padx=10, anchor=W)

        self.button_MLCLS_setas_category = tk.Button(self.frame_MLCLS_row1_options_mid,
                                                     text="Change selected to category type", height=1, width=25,
                                                     command=self.change_to_category_MLCLS)
        self.button_MLCLS_setas_category.pack(pady=3, padx=10, anchor=W)

        self.frame_MLCLS_row1_options_algorithms = tk.Frame(self.frame_MLCLS_row1_options_mid, borderwidth=0,
                                                            highlightthickness=0, highlightbackground="yellow")
        self.frame_MLCLS_row1_options_algorithms.pack(pady=20, ipady=3)
        self.label_MLCLS_algorithm = tk.Label(self.frame_MLCLS_row1_options_algorithms, text="Algorithm:")
        self.label_MLCLS_algorithm.pack(side=LEFT)

        self.var_MLCLS_algorithm = tk.StringVar()
        self.combobox_MLCLS_algorithm = ttk.Combobox(self.frame_MLCLS_row1_options_algorithms,
                                                     textvariable=self.var_MLCLS_algorithm,
                                                     values=[MlAlgorithms.SVM, MlAlgorithms.LOG_REGRESSION,
                                                             MlAlgorithms.DECISION_TREE], state="readonly")
        self.combobox_MLCLS_algorithm.current(1)
        self.combobox_MLCLS_algorithm.pack(side=LEFT)
        self.selected_MLCLS_target_column = helper_object_ml_cls.get_selected_target_column()

        self.frame_MLCLS_row1_options_parent = tk.Frame(self.frame_MLCLS_row1)
        self.frame_MLCLS_row1_options_parent.pack(side=LEFT, pady=2, padx=20)

        self.frame_MLCLS_row1_options = tk.LabelFrame(self.frame_MLCLS_row1_options_parent, text="Options")
        self.frame_MLCLS_row1_options.pack(pady=2, padx=20)
        self.classification_model = None
        self.var_MLCLS_options_shuffle = tk.IntVar()
        self.var_MLCLS_options_shuffle.set(1)
        self.checkbutton_MLCLS_options_shuffle = tk.Checkbutton(self.frame_MLCLS_row1_options, text="Shuffle data",
                                                                variable=self.var_MLCLS_options_shuffle)
        self.checkbutton_MLCLS_options_shuffle.pack(anchor=W, padx=5)

        self.var_MLCLS_options_encode_label = tk.IntVar()
        self.var_MLCLS_options_encode_label.set(1)
        self.checkbutton_MLCLS_options_encode_label = tk.Checkbutton(self.frame_MLCLS_row1_options, text="Encode Label",
                                                                     variable=self.var_MLCLS_options_encode_label)
        self.checkbutton_MLCLS_options_encode_label.pack(anchor=W, padx=5)

        self.var_MLCLS_options_onehot_encode = tk.IntVar()
        self.var_MLCLS_options_onehot_encode.set(1)
        self.checkbutton_MLCLS_options_onehot_encode = tk.Checkbutton(self.frame_MLCLS_row1_options,
                                                                      text="Onehot Encode Categorical",
                                                                      variable=self.var_MLCLS_options_onehot_encode)
        self.checkbutton_MLCLS_options_onehot_encode.pack(anchor=W, padx=5)

        self.frame_MLCLS_row1_data_split_options = tk.Frame(self.frame_MLCLS_row1)
        self.frame_MLCLS_row1_data_split_options.pack(side=LEFT, pady=2, padx=20)

        self.frame_MLCLS_row1_buttons_data_split = tk.LabelFrame(self.frame_MLCLS_row1_data_split_options,
                                                                 text="Train -Test Split")
        self.frame_MLCLS_row1_buttons_data_split.pack(ipadx=10, padx=5, ipady=5)

        self.label_MLCLS_train_test_split_data = tk.Label(self.frame_MLCLS_row1_buttons_data_split,
                                                          text="Train:80%       Test:20%")
        self.label_MLCLS_train_test_split_data.pack(pady=5)
        self.var_MLCLS_train_test_input = tk.DoubleVar()
        self.slider_MLCLS_train_test_split = tk.Scale(self.frame_MLCLS_row1_buttons_data_split,
                                                      variable=self.var_MLCLS_train_test_input,
                                                      from_=1, to=99, orient=HORIZONTAL,
                                                      command=self.update_traintest_split_slider, length=150,
                                                      showvalue=False)
        self.slider_MLCLS_train_test_split.set(80)
        self.slider_MLCLS_train_test_split.pack()

        self.frame_MLCLS_train_test_split_rs = tk.Frame(self.frame_MLCLS_row1_buttons_data_split)
        self.frame_MLCLS_train_test_split_rs.pack(side=LEFT, pady=10)

        self.label_MLCLS_train_test_split_rs = tk.Label(self.frame_MLCLS_train_test_split_rs,
                                                        text="Random State:").pack(side=LEFT)
        self.var_MLCLS_random_state = tk.IntVar()
        self.combobox_MLCLS_random_state = ttk.Combobox(self.frame_MLCLS_train_test_split_rs,
                                                        textvariable=self.var_MLCLS_random_state,
                                                        values=[i for i in range(1000)], width=4)
        self.combobox_MLCLS_random_state.current(42)
        self.combobox_MLCLS_random_state.pack(side=LEFT)

        self.button_MLCLS_train_model = tk.Button(self.frame_MLCLS_row1_options_parent, text="Train Model",
                                                  command=self.start_MCLS_training, height=2, width=30)
        self.button_MLCLS_train_model.pack(pady=10)

        self.frame_MLCLS_row2 = tk.Frame(self.tab_ml_classification, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_MLCLS_row2.pack(fill=X, padx=3)

        label_MLCLS_train_test_split_heading = tk.Label(self.frame_MLCLS_row2,
                                                        text="Train Results").pack()
        self.text_MLCLS_train_results = tk.Text(self.frame_MLCLS_row2, height=20, width=120)
        self.text_MLCLS_train_results.pack(padx=3, pady=2)

        self.frame_MLCLS_row3 = tk.Frame(self.tab_ml_classification, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_MLCLS_row3.pack(fill=X, padx=10, pady=15, ipady=5)
        self.button_MLCLS_show_confusion_matrix = tk.Button(self.frame_MLCLS_row3, text="Show Confusion Matrix",
                                                            height=2, width=20, command=self.show_confusion_matrix)
        self.button_MLCLS_show_confusion_matrix.pack(side=LEFT, padx=10, ipady=5)
        self.button_MLCLS_export_model = tk.Button(self.frame_MLCLS_row3, text="Export Model", height=2, width=20,
                                                   command=self.export_model)
        self.button_MLCLS_export_model.pack(side=LEFT, padx=10, ipady=5)
        self.button_MLCLS_export_predicted_data = tk.Button(self.frame_MLCLS_row3, text="Export Final Data (X)",
                                                            height=2,
                                                            width=20, command=self.export_data_X)
        self.button_MLCLS_export_predicted_data.pack(side=LEFT, padx=10, ipady=5)
        self.button_MLCLS_export_model_to_pred = tk.Button(self.frame_MLCLS_row3, text="Pass Model to Prediction Tab",
                                                           height=2,
                                                           width=24, command=self.export_model_to_pred)
        self.button_MLCLS_export_model_to_pred.pack(side=LEFT, padx=10, ipady=5)
        self.var_mapping_MLCLS_le = None
        self.button_MLCLS_export_le_mapping = tk.Button(self.frame_MLCLS_row3, text="Export Label Encode Mapping",
                                                        height=2,
                                                        width=24, command=self.export_label_encode_mapping)
        self.button_MLCLS_export_le_mapping.pack(side=LEFT, padx=10, ipady=5)

    def add_MLCLS_target(self):
        if (len(self.listbox_MLCLS_available_columns.curselection()) > 0):
            currentitem = self.listbox_MLCLS_available_columns.get(ACTIVE)
            helper_object_ml_cls.set_selected_target_column(currentitem)
            self.selected_MLCLS_target_column = currentitem
            self.label_MLCLS_target_var.configure(text=self.selected_MLCLS_target_column)
        else:
            messagebox.showerror("No items selected", "Please select a value from the list of available columns.")

    def change_to_category_MLCLS(self):
        if (len(self.listbox_MLCLS_available_columns.curselection()) > 0):
            currentitem = self.listbox_MLCLS_available_columns.get(ACTIVE)
            print(currentitem, type(currentitem))
            helper_object_ml_cls.get_data_process_obj().dframe[currentitem] = \
                helper_object_ml_cls.get_data_process_obj().dframe[currentitem].astype('category')
            helper_object_ml_cls.get_data_process_obj().sync_dframe()
            messagebox.showinfo("Success", f"The column:{currentitem} has been changed to category data type.")

        else:
            messagebox.showerror("No items selected", "Please select a value from the list of available columns.")

    def update_traintest_split_slider(self, slider_value):
        self.label_MLCLS_train_test_split_data.config(
            text=f"Train:{int(slider_value):02}%  Test:{100 - int(slider_value):02}%")

    def start_MCLS_training(self):
        df = helper_object_ml_cls.get_dframe()
        target = helper_object_ml_cls.get_selected_target_column()
        selected_features = helper_object_ml_cls.get_selected_features_list()

        if df is None or len(selected_features) == 0 or target == None:
            messagebox.showerror("Error", "Please load data,confirm features and select target column before training.")
        else:
            try:
                self.text_MLCLS_train_results.delete('1.0', END)
                if target in selected_features:
                    selected_features.remove(target)
                if self.var_MLCLS_options_shuffle.get() == 1:
                    shuffle_required = True
                else:
                    shuffle_required = False

                self.X = df[selected_features]
                self.y = df[target]
                # --applying encode
                if self.var_MLCLS_options_encode_label.get() == 1:
                    le = LabelEncoder()
                    self.y = le.fit_transform(self.y)

                    self.var_mapping_MLCLS_le = dict(zip(le.transform(le.classes_), le.classes_))
                    self.text_MLCLS_train_results.insert(END,
                                                         f'>>Target Label Encode Mapping:\n {self.var_mapping_MLCLS_le}\n')
                if self.var_MLCLS_options_onehot_encode.get() == 1:
                    # Get one hot encoding of categorical columns
                    categorical_columns = self.X.select_dtypes(include=['object', 'category']).columns.tolist()
                    if categorical_columns:
                        one_hot = pd.get_dummies(self.X[categorical_columns])
                        # Drop columns as it is now encoded
                        self.X = self.X.drop(categorical_columns, axis=1)
                        # Join the encoded df
                        self.X = self.X.join(one_hot)

                # train test split
                self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y,
                                                                                        shuffle=shuffle_required,
                                                                                        train_size=self.var_MLCLS_train_test_input.get() / 100,
                                                                                        random_state=self.var_MLCLS_random_state.get())

                if self.var_MLCLS_algorithm.get() == MlAlgorithms.DECISION_TREE:
                    self.classification_model = DecisionTreeClassifier()
                elif self.var_MLCLS_algorithm.get() == MlAlgorithms.SVM:
                    self.classification_model = SVC()
                elif self.var_MLCLS_algorithm.get() == MlAlgorithms.LOG_REGRESSION:
                    self.classification_model = LogisticRegression()
                self.text_MLCLS_train_results.insert(END,
                                                     f'>> Data splitted into Train-Test data in the ratio {self.var_MLCLS_train_test_input.get()}:{100 - self.var_MLCLS_train_test_input.get()}')
                # training model
                self.text_MLCLS_train_results.insert(END,
                                                     f'\n>> Training started using the algorithm: {self.var_MLCLS_algorithm.get()} at {str(datetime.now())}.')
                self.classification_model.fit(self.X_train, self.y_train)
                # predict
                self.model_prediction = self.classification_model.predict(self.X_test)
                self.text_MLCLS_train_results.insert(END, f'\n>> Training completed at {str(datetime.now())}.\n')
                self.text_MLCLS_train_results.insert(END, '\n>> Trained Model Summary:\n')
                self.text_MLCLS_train_results.insert(END, '-' * 25)
                # checking accuracy
                self.text_MLCLS_train_results.insert(END,
                                                     f'\n Accuracy_score: {accuracy_score(self.model_prediction, self.y_test)}')
                self.text_MLCLS_train_results.insert(END,
                                                     f'\n Confusion_matrix:\n {confusion_matrix(self.model_prediction, self.y_test)}')
                self.text_MLCLS_train_results.insert(END,
                                                     f'\n Classification_report:\n {classification_report(self.model_prediction, self.y_test)}')

                self.text_MLCLS_train_results.insert(END, '--' * 50)
                helper_object_ml_cls.update_bottom_status_bar('Classification model training done.')
            except Exception as err:
                messagebox.showerror("Error", f"Unable do the requested action.{str(err)}")
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def show_confusion_matrix(self):
        if self.classification_model is None:
            messagebox.showerror("Model not trained", "The model is not trained. Please train it.")
        else:
            try:
                # plot confusion matrix
                disp = ConfusionMatrixDisplay.from_estimator(
                    self.classification_model,
                    self.X_test,
                    self.y_test,
                    cmap=plt.cm.Blues,
                )
                disp.ax_.set_title("Confusion Matrix")
                plt.show()
            except Exception as err:
                messagebox.showerror("Error", f"Unable to plot.{str(err)}")
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def export_model(self):
        if self.classification_model is None:
            messagebox.showerror("Model not trained", "The model is not trained. Please train before exporting.")
        else:
            try:
                file_dialog = filedialog.asksaveasfile(mode='w',
                                                       defaultextension=f".{configurable_constants.MODEL_EXPORT_EXTENSION}")
                if file_dialog is None:
                    return
                pickle.dump(self.classification_model, open(file_dialog.name, 'wb'))
                messagebox.showinfo("Exported", f"Model exported to the path : {file_dialog.name}")
            except Exception as err:
                messagebox.showerror("Error", f"Unable do the requested action.{str(err)}")
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
                messagebox.showerror("Error", f"Unable do the requested action.{str(err)}")
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def export_model_to_pred(self):
        if self.classification_model is None:
            messagebox.showerror("Model not trained", "The model is not trained. Please train before exporting.")
        else:
            try:
                helper_object_ml_cls.get_ml_predict_obj().model_MLPRED_CLS = self.classification_model
                helper_object_ml_cls.get_ml_predict_obj().label_MLPRED_CLS_model_status.configure(
                    text=f"{helper_object_ml_cls.get_ml_predict_obj().model_MLPRED_CLS} - Model imported from training tab.",
                    fg="green")
                messagebox.showinfo("Exported", "Model pushed to prediction")
            except Exception as err:
                messagebox.showerror("Error", f"Unable to export model.{str(err)}")
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def export_label_encode_mapping(self):
        if self.var_mapping_MLCLS_le is None:
            messagebox.showerror("Model not trained", "Please train before exporting.")
        else:
            try:
                file_dialog = filedialog.asksaveasfile(mode='w',
                                                       defaultextension=f".{configurable_constants.LABEL_ENCODE_EXPORT_EXTENSION}")
                if file_dialog is None:
                    return
                file_dialog.write(json.dumps({str(k): v for k, v in self.var_mapping_MLCLS_le.items()}))
                file_dialog.close()
                messagebox.showinfo("Exported", f"Label Encode Mapping exported to the path : {file_dialog.name}")
            except Exception as err:
                messagebox.showerror("Error", f"Unable do the requested action.{str(err)}")
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))
