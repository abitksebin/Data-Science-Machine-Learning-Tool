# -------------------------------------------------------------------------------
# Name:        configurable_constants.py
# Purpose:     To define constants (including string contstants)
# Project:     dsmltool - BITS M.Tech Dissertation
# Author:      Abit K Sebin
#
# Created:     Jun - Aug 2022
# Copyright:   (c) abitk 2022
# Licence:     <None>
# -------------------------------------------------------------------------------
import logging

SW_VER = '0.1'
SW_TITLE = "Data Science & Machine Learning Tool"
SPLASH_DELAY = .5  # similated delay in seconds for splash screen
CONFIG_FILE_NAME = "config.ini"
DEFAULT_CONFIG_VALUES = {"splash_on": "True", "hide_console": "False", "welcome_on": "True"}
LOG_FILE_NAME = "Execution_logs.log"
NONACTIVE_TAB_BG_COLOR = "#3C3B3A"
ACTIVE_TAB_BG_COLOR = "blue"
DELIMITER = ','
LOGGING_LEVEL_FILE = logging.ERROR  # logging.INFO
LOGGING_LEVEL_STREAM = logging.ERROR  # logging.INFO
MODEL_EXPORT_EXTENSION = "dsmlt"
LABEL_ENCODE_EXPORT_EXTENSION = "lemap"
WELCOME_TEXT = "Welcome to the " + SW_TITLE + " for non-programmers. This tool " \
                                              "can be used to perform data science tasks from preprocessing to" \
                                              " machine learning prediction. The tool has the options to combine " \
                                              "multiple files, do the preprocessing such as cleaning data by removing" \
                                              " blanks,nulls and duplicates, remove outlier values, missing data imputation," \
                                              "onehot encoding etc. It has various data analysis options such as viewing " \
                                              "multiple information about data, plotting different types of graphs to find " \
                                              "the relations in data,  correlations analysis etc. It has feature selection " \
                                              "functionalities . This tool allows to do machine learning (classification, " \
                                              "regression and clustering) using different algorithms. It also provides the " \
                                              "functionality to export the trained models for future use. The exported models " \
                                              "can be imported to do prediction on a different dataset."
# --------------------Info Messages--------------------------------------------------------
Info_Msg_Content_1 = "Data from multiple CSV files can be used in this tool for analysis. This section allows to select a CSV file or multiple CSV files."
Info_Msg_Content_2 = "The outliers in each selected column can be removed using 1.5xIQR method."
Info_Msg_Content_3 = ("The processed data can be used for further analysis by plotting multiple graphs."
                      " This section shows the correlation between the features. ")
Info_Msg_Content_4 = "Scatter plot is used to check the relation between two columns."
Info_Msg_Content_5 = ("You can plot Line Plot, Histogram or Kernel Density Estimation graphs using this feature. "
                      "Add the columns required for plotting and click on the corresponding graph button to view the graph.")
Info_Msg_Content_6 = ("Pearson correlation coefficient is a measure of the strength of a linear association between"
                      " two variables. It can take a range of values from +1 to -1. A value of 0 indicates that there is no association between"
                      " the two variables.A value greater than 0 indicates a positive association; that is, as the value of one variable increases,"
                      " so does the value of the other variable. A value less than 0 indicates a negative association; that is, as the value of "
                      "one variable increases, the value of the other variable decreases.")
