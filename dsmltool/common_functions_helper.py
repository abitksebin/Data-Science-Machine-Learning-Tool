# -------------------------------------------------------------------------------
# Name:        common_functions_helper.py
# Purpose:     Common functionalities
# Project:     dsmltool - BITS M.Tech Dissertation
# Author:      Abit K Sebin
#
# Created:     Jun - Aug 2022
# Copyright:   (c) abitk 2022
# Licence:     <None>
# -------------------------------------------------------------------------------
import configparser
import logging
import os
from tkinter import END

import pandas as pd

import configurable_constants


class Helper:
    """Class that has the common methods """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Helper.__instance is None:
            Helper()
        return Helper.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Helper.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Helper.__instance = self
        self.config_file_name = configurable_constants.CONFIG_FILE_NAME
        self.config = self.read_configuration_file()
        self.logger = self.create_custom_logger()
        self.dframe = pd.DataFrame()
        self.data_process_obj = None
        self.data_analysis_obj = None
        self.feature_selection_obj = None
        self.ml_classification_obj = None
        self.selected_features_list = []
        self.label_footer_df_status = None
        self.selected_target_column = None
        self.label_footer_status_label = None
        self.ml_predict_obj = None

    @staticmethod
    def log_format(file_name, fn_name, msg):
        return str(msg) + ' ( File:' + file_name + ' Func:' + fn_name + ')'

    def set_selected_target_column(self, selected_target_column):
        self.selected_target_column = selected_target_column

    def get_selected_target_column(self):
        return self.selected_target_column

    def set_data_process_obj(self, dataprocess_obj):
        self.data_process_obj = dataprocess_obj

    def get_data_process_obj(self):
        return self.data_process_obj

    def set_data_analysis_obj(self, data_analysis_obj):
        self.data_analysis_obj = data_analysis_obj

    def get_data_analysis_obj(self):
        return self.data_analysis_obj

    def set_feature_selection_obj(self, feature_selection_obj):
        self.feature_selection_obj = feature_selection_obj

    def get_feature_selection_obj(self):
        return self.feature_selection_obj

    def set_ml_classification_obj(self, ml_classification_obj):
        self.ml_classification_obj = ml_classification_obj

    def get_ml_classification_obj(self):
        return self.ml_classification_obj

    def set_ml_clustering_obj(self, ml_clustering_obj):
        self.ml_clustering_obj = ml_clustering_obj

    def get_ml_clustering_obj(self):
        return self.ml_clustering_obj

    def set_ml_regression_obj(self, ml_regression_obj):
        self.ml_regression_obj = ml_regression_obj

    def get_ml_regression_obj(self):
        return self.ml_regression_obj

    def set_ml_predict_obj(self, ml_predict_obj):
        self.ml_predict_obj = ml_predict_obj

    def get_ml_predict_obj(self):
        return self.ml_predict_obj

    def get_config_file_name(self):
        return self.config_file_name

    def read_configuration_file(self):
        config = configparser.ConfigParser()
        fileread = config.read(self.config_file_name)
        if len(fileread) < 1:
            def populate_default_config_file():
                default_config = configurable_constants.DEFAULT_CONFIG_VALUES
                config.add_section('RUN')
                for key in default_config.keys():
                    config.set('RUN', key, default_config[key])
                with open(self.config_file_name, 'w') as f:
                    config.write(f)

            populate_default_config_file()
        return config

    def write_configuration_file(self):
        with open(self.config_file_name, 'w') as configfile:  # save
            self.config.write(configfile)

    def get_configuration(self):
        return self.config

    def create_custom_logger(self):
        # Creating a custom logger
        logger = logging.getLogger(configurable_constants.SW_TITLE)
        # Creating handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(configurable_constants.LOG_FILE_NAME)
        c_handler.setLevel(configurable_constants.LOGGING_LEVEL_STREAM)
        f_handler.setLevel(configurable_constants.LOGGING_LEVEL_FILE)
        # Creating formatters for handlers
        c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)
        # Adding handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        return logger

    def get_logger(self):
        return self.logger

    def get_dframe(self):
        return self.dframe

    def set_dframe(self, dframe):
        self.dframe = dframe

    def ensure_dir(self, file_path):
        """Function that creates folder if it doesn't exist """
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("New folder created")

    def set_selected_features_list(self, selected_features_list):
        self.selected_features_list = selected_features_list

    def get_selected_features_list(self):
        return self.selected_features_list

    def update_bottom_status_bar(self, text_string, msg_type='INFO'):
        """Function that updates application status bar """
        self.label_footer_status_label.configure(text=msg_type + ':')
        self.label_footer_df_status.configure(
            text=text_string)

    def populate_confirmed_feature_columns_in_tabs(self):
        """Function that populate confirmed features in the ML training tabs """
        # load features for classification
        self.get_ml_classification_obj().listbox_MLCLS_available_columns.delete(0, END)
        for col in self.get_selected_features_list():
            self.get_ml_classification_obj().listbox_MLCLS_available_columns.insert(END, col)
        self.get_ml_classification_obj().listbox_MLCLS_available_columns.insert(END, self.get_selected_target_column())
        self.get_ml_classification_obj().label_MLCLS_target_var.configure(
            text=self.get_selected_target_column())
        # load features for clustering
        self.get_ml_clustering_obj().listbox_MLCLR_available_columns.delete(0, END)
        for col in self.get_selected_features_list():
            self.get_ml_clustering_obj().listbox_MLCLR_available_columns.insert(END, col)
        self.get_ml_clustering_obj().listbox_MLCLR_available_columns.insert(END, self.get_selected_target_column())
        # load features for regression
        self.get_ml_regression_obj().listbox_MLREG_available_columns.delete(0, END)
        for col in self.get_selected_features_list():
            self.get_ml_regression_obj().listbox_MLREG_available_columns.insert(END, col)
        self.get_ml_regression_obj().listbox_MLREG_available_columns.insert(END, self.get_selected_target_column())
        self.get_ml_regression_obj().label_MLREG_target_var.configure(
            text=self.get_selected_target_column())
