# -------------------------------------------------------------------------------
# Name:        data_analyis.py
# Purpose:     Data Analysis Tab code of the tool
# Project:     dsmltool - BITS M.Tech Dissertation
# Author:      Abit K Sebin
#
# Created:     Jun - Aug 2022
# Copyright:   (c) abitk 2022
# Licence:     <None>
# -------------------------------------------------------------------------------

import tkinter as tk
from functools import partial
from tkinter import END, LEFT, RIGHT, X, Y, ACTIVE, messagebox

import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import configurable_constants
from common_functions_helper import Helper

log = Helper.getInstance().get_logger()
helper_object_da = Helper.getInstance()


class DataAnalysis:
    """Class that has all UI components and variables for Data Analysis Tab """

    def __init__(self, tab_data_analysis):
        self.tab_data_analysis = tab_data_analysis
        self.tab2_frame_section1 = tk.Frame(tab_data_analysis)
        self.data_visualisation_controls()
        self.frame_section4_DA = tk.Frame(tab_data_analysis, borderwidth=1, highlightthickness=0,
                                          highlightbackground="black")
        self.frame_section4_DA.pack(fill=X)
        self.frame_section4_analysis = tk.LabelFrame(self.frame_section4_DA, borderwidth=1, highlightthickness=0,
                                                     highlightbackground="red", text="Further Analysis Options ")
        self.frame_section4_analysis.pack(padx=10, pady=10, ipady=2, fill=X)
        self.button_info_analysis = tk.Button(self.frame_section4_analysis, font='Helvetica 8 italic', text="Help",
                                              fg="white",
                                              bg="grey", borderwidth=0, command=self.showanalysisinfo)
        self.button_info_analysis.pack(side=RIGHT, anchor="n")
        self.frame_section4_analysis_ln1 = tk.Frame(self.frame_section4_analysis)
        self.frame_section4_analysis_ln1.pack(side=LEFT)

        self.button_correlationMatrix = tk.Button(self.frame_section4_analysis_ln1, text="Show Correlation Matrix",
                                                  command=self.pccMatrixGraph,
                                                  width=25, height=2)
        self.button_correlationMatrix.pack(pady=5, padx=25, side=LEFT)

    @staticmethod
    def showanalysisinfo():
        messagebox.showinfo("Data Analysis - Information", configurable_constants.Info_Msg_Content_3)

    @staticmethod
    def showscatterinfo():
        messagebox.showinfo("Scatter Plot - Information", configurable_constants.Info_Msg_Content_4)

    @staticmethod
    def showgraphinfo():
        messagebox.showinfo("Graphs - Information", configurable_constants.Info_Msg_Content_5)

    @staticmethod
    def showpccinfo():
        messagebox.showinfo("PCC - Information", configurable_constants.Info_Msg_Content_6)

    def data_visualisation_controls(self):
        dframe = helper_object_da.get_dframe()
        self.data_visualisation_controls_lf = tk.LabelFrame(self.tab_data_analysis, text="Data Visualization")
        self.data_visualisation_controls_lf.pack(padx=10, pady=10, ipady=2, fill=X)

        self.frame_graph_info = tk.Frame(self.data_visualisation_controls_lf, borderwidth=0, highlightthickness=0,
                                         highlightbackground="red")
        self.frame_graph_info.pack(fill=X)
        self.label_graph_infoanalysis = tk.Label(self.frame_graph_info, font='Helvetica 8 italic',
                                                 text="Select columns required for plotting and click on the graph buttons (Scatter plot, Line Plot, Histogram, Box Plot or Kernel Density Estimation) to plot the graph.")
        self.label_graph_infoanalysis.pack(side=LEFT, pady=15, padx=15)
        self.button_graph_info_analysis = tk.Button(self.frame_graph_info, font='Helvetica 8 italic', text="Help",
                                                    fg="white",
                                                    bg="grey", borderwidth=0, command=self.showgraphinfo)
        self.button_graph_info_analysis.pack(side=RIGHT)
        self.frame_graph_sec1 = tk.Frame(self.data_visualisation_controls_lf, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_graph_sec1.pack(anchor='center', pady=15)
        self.frame_graph_sec1_ls = tk.Frame(self.frame_graph_sec1, borderwidth=0, highlightthickness=0,
                                            highlightbackground="blue")
        self.frame_graph_sec1_ls.pack(side=LEFT)
        self.frame_graph_sec1_mid = tk.Frame(self.frame_graph_sec1, borderwidth=0, highlightthickness=0,
                                             highlightbackground="red")
        self.frame_graph_sec1_mid.pack(side=LEFT, padx=10)
        self.frame_graph_sec1_rs = tk.Frame(self.frame_graph_sec1, borderwidth=0, highlightthickness=0,
                                            highlightbackground="red")
        self.frame_graph_sec1_rs.pack(side=LEFT)
        self.label_graph_available_headers = tk.Label(self.frame_graph_sec1_ls,
                                                      text="Select column header form the list")
        self.label_graph_available_headers.pack()
        self.scrollbar_graph_available_headers = tk.Scrollbar(self.frame_graph_sec1_ls)
        self.scrollbar_graph_available_headers.pack(side=RIGHT, fill=Y)
        self.listbox_graph_available_headers = tk.Listbox(self.frame_graph_sec1_ls, width=40,
                                                          yscrollcommand=self.scrollbar_graph_available_headers.set,
                                                          height=10)
        self.listbox_graph_available_headers.pack()
        self.scrollbar_graph_available_headers.config(command=self.listbox_graph_available_headers.yview)
        self.listbox_graph_available_headers.delete(0, END)
        for col in helper_object_da.get_dframe().columns:
            self.listbox_graph_available_headers.insert(END, col)
        self.button_graph_addto_list = tk.Button(self.frame_graph_sec1_mid, text="Add selected column\t >",
                                                 height=1, width=24,
                                                 command=self.addtoGraphlist)
        self.button_graph_addto_list.pack(pady=1, padx=10)
        self.button_graph_addto_list = tk.Button(self.frame_graph_sec1_mid, text="Remove selected column\t <",
                                                 height=1, width=24,
                                                 command=self.removefromGraphlist)
        self.button_graph_addto_list.pack(pady=1, padx=10)
        self.button_graph_addto_list = tk.Button(self.frame_graph_sec1_mid, text="Add all columns\t\t >>", height=1,
                                                 width=24,
                                                 command=self.addalltoGraphlist)
        self.button_graph_addto_list.pack(pady=1, padx=10)
        self.button_graph_addto_list = tk.Button(self.frame_graph_sec1_mid, text="Remove all columns\t <<",
                                                 height=1, width=24,
                                                 command=self.removeallfromGraphlist)
        self.button_graph_addto_list.pack(pady=1, padx=10)
        self.label_graph_var = tk.Label(self.frame_graph_sec1_rs, text="Columns selected for plotting")
        self.label_graph_var.pack()
        self.scrollbar_graph_var = tk.Scrollbar(self.frame_graph_sec1_rs)
        self.scrollbar_graph_var.pack(side=RIGHT, fill=Y)
        self.listbox_graph_var = tk.Listbox(self.frame_graph_sec1_rs, width=40, height=10,
                                            yscrollcommand=self.scrollbar_graph_var.set)
        self.listbox_graph_var.pack(padx=10)
        self.scrollbar_graph_var.config(command=self.listbox_graph_var.yview)
        self.frame_graph_sec2 = tk.Frame(self.data_visualisation_controls_lf, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_graph_sec2.pack(pady=15, anchor='center')
        self.var_removeoutlierbeforeplot = tk.IntVar()
        self.checkbutton_removeoutlierbeforeplot = tk.Checkbutton(self.frame_graph_sec2,
                                                                  text="Remove outliers from graph",
                                                                  variable=self.var_removeoutlierbeforeplot,
                                                                  width=20)
        self.checkbutton_removeoutlierbeforeplot.pack(pady=4)
        self.var_seperate_plot = tk.IntVar()
        self.checkbutton_seperate_plot = tk.Checkbutton(self.frame_graph_sec2,
                                                        text="Seperate Plots (Not applicable for Scatter plot and Box plot)",
                                                        variable=self.var_seperate_plot)
        self.checkbutton_seperate_plot.pack(pady=4)

        self.button_graph_line = tk.Button(self.frame_graph_sec2, width=25, text="Line Plot", height=2,
                                           command=partial(self.linePlot, self.data_visualisation_controls_lf))
        self.button_graph_line.pack(padx=10, side=LEFT)

        self.button_graph_scatterplot = tk.Button(self.frame_graph_sec2, width=25, text="Scatter Plot", height=2,
                                                  command=partial(self.scatterPlot,
                                                                  self.data_visualisation_controls_lf))
        self.button_graph_scatterplot.pack(padx=10, side=LEFT)

        self.button_graph_histogram = tk.Button(self.frame_graph_sec2, width=25, text="Histogram", height=2,
                                                command=partial(self.histogram, self.data_visualisation_controls_lf))
        self.button_graph_histogram.pack(padx=10, side=LEFT)
        self.button_graph_histogram = tk.Button(self.frame_graph_sec2, width=25, text="Kernel Density Estimation",
                                                height=2,
                                                command=partial(self.kdp, self.data_visualisation_controls_lf))
        self.button_graph_histogram.pack(padx=10, side=LEFT)
        self.button_graph_boxplot = tk.Button(self.frame_graph_sec2, width=25, text="Box Plot", height=2,
                                              command=partial(self.boxplot, self.data_visualisation_controls_lf))
        self.button_graph_boxplot.pack(padx=10, side=LEFT)
        self.label_graph_error = tk.Label(self.data_visualisation_controls_lf, text="")
        self.label_graph_error.pack()

    def update_column_list_in_ctrl(self):
        self.listbox_graph_available_headers.delete(0, END)
        for col in helper_object_da.get_dframe().columns:
            self.listbox_graph_available_headers.insert(END, col)

    def addtoGraphlist(self):
        if (len(self.listbox_graph_available_headers.curselection()) > 0):
            currentitem = self.listbox_graph_available_headers.get(ACTIVE)
            if not currentitem in self.listbox_graph_var.get(0, END):
                self.listbox_graph_var.insert(0, currentitem)
                self.label_graph_error.configure(text="")

    def removefromGraphlist(self):
        if (len(self.listbox_graph_var.curselection()) > 0):
            self.listbox_graph_var.delete(self.listbox_graph_var.curselection())

    def addalltoGraphlist(self):
        for items in self.listbox_graph_available_headers.get(0, END):
            if not items in self.listbox_graph_var.get(0, END):
                self.listbox_graph_var.insert(END, items)
        self.label_graph_error.configure(text="")

    def removeallfromGraphlist(self):
        self.listbox_graph_var.delete(0, END)

    def linePlot(self, top_graph):
        list_of_columns = list(self.listbox_graph_var.get(0, END))
        if len(list_of_columns) < 1:
            self.label_graph_error.configure(
                text="Minimum one column is required for graph. Please select at least one columns.", fg="red")
        else:
            try:
                self.label_graph_error.configure(text="")
                dfp = helper_object_da.get_dframe()[list_of_columns]
                if self.var_removeoutlierbeforeplot.get() == 1:
                    for cols in list_of_columns:
                        df_temp = helper_object_da.get_data_process_obj().get_1_5_IQR(dfp, cols)
                        dfp = df_temp
                top_line = tk.Toplevel(top_graph)
                top_line.attributes('-topmost', True)
                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                if self.var_seperate_plot.get() == 1:
                    dfp.plot(title="Line Plot", subplots=True, grid=True, use_index=True, ax=ax)
                else:
                    dfp.plot(title="Line Plot", grid=True, use_index=True, ax=ax)
                ax.set_xlabel("Time/Index")  # X label
                ax.set_ylabel("Values")  # X label
                canvas = FigureCanvasTkAgg(fig, master=top_line)
                canvas.draw()
                canvas.get_tk_widget().pack()
            except Exception as err:
                print("Line Plot Error:", err)
                messagebox.showerror("Line Plot Error",
                                     "Unable to plot the graph. Please try again with different data.")

    def histogram(self, top_graph):
        dframe = helper_object_da.get_dframe()
        list_of_columns = list(self.listbox_graph_var.get(0, END))
        if len(list_of_columns) < 1:
            self.label_graph_error.configure(
                text="Minimum one column is required for graph. Please select at least one columns.", fg="red")
        else:
            try:
                self.label_graph_error.configure(text="")
                dfp = dframe[list_of_columns]
                if self.var_removeoutlierbeforeplot.get() == 1:
                    for cols in list_of_columns:
                        df_temp = helper_object_da.get_data_process_obj().get_1_5_IQR(dfp, cols)
                        dfp = df_temp
                top_line_hist = tk.Toplevel(top_graph)
                top_line_hist.attributes('-topmost', True)
                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                ax.set_xlabel("Data Value Ranges")  # X label
                if self.var_seperate_plot.get() == 1:
                    dfp.plot.hist(alpha=0.5, title="Histogram", subplots=True, grid=True, ax=ax)
                else:
                    dfp.plot.hist(alpha=0.5, title="Histogram", grid=True, ax=ax)

                canvas = FigureCanvasTkAgg(fig, master=top_line_hist)
                canvas.draw()
                canvas.get_tk_widget().pack()
            except Exception as err:
                print("Histogram Error:", err)
                messagebox.showerror("Histogram Plot Error",
                                     "Unable to plot the graph. Please try again with different data.")

    def boxplot(self, top_graph):
        dframe = helper_object_da.get_dframe()
        list_of_columns = list(self.listbox_graph_var.get(0, END))
        if len(list_of_columns) < 1:
            self.label_graph_error.configure(
                text="Minimum one column is required for graph. Please select at least one columns.", fg="red")
        else:
            try:
                self.label_graph_error.configure(text="")
                dfp = dframe[list_of_columns]
                if self.var_removeoutlierbeforeplot.get() == 1:
                    for cols in list_of_columns:
                        df_temp = helper_object_da.get_data_process_obj().get_1_5_IQR(dfp, cols)
                        dfp = df_temp
                if len(list_of_columns) > 6:
                    graph_rot = 45
                else:
                    graph_rot = 0
                top_line_hist = tk.Toplevel(top_graph)
                top_line_hist.attributes('-topmost', True)
                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                dfp.boxplot(grid=True, ax=ax, rot=graph_rot)
                ax.set_xlabel("Parameter(s)")  # X label
                ax.set_ylabel("Data Values")  # Y label
                canvas = FigureCanvasTkAgg(fig, master=top_line_hist)
                canvas.draw()
                canvas.get_tk_widget().pack()
            except Exception as err:
                print("Box plot Error:", err)
                messagebox.showerror("Box Plot Error",
                                     "Unable to plot the graph. Please try again with different data.")

    def kdp(self, top_graph):
        dframe = helper_object_da.get_dframe()
        list_of_columns = list(self.listbox_graph_var.get(0, END))
        if len(list_of_columns) < 1:
            self.label_graph_error.configure(
                text="Minimum one column is required for graph. Please select at least one columns.", fg="red")
        else:
            try:
                self.label_graph_error.configure(text="")
                dfp = dframe[list_of_columns]
                if self.var_removeoutlierbeforeplot.get() == 1:
                    for cols in list_of_columns:
                        df_temp = helper_object_da.get_data_process_obj().get_1_5_IQR(dfp, cols)
                        dfp = df_temp
                top_line_kdp = tk.Toplevel(top_graph)
                top_line_kdp.attributes('-topmost', True)
                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                if self.var_seperate_plot.get() == 1:
                    dfp.plot.kde(title="Kernel Density Estimation", subplots=True, ax=ax, grid=True)
                else:
                    dfp.plot.kde(title="Kernel Density Estimation", ax=ax, grid=True)
                ax.set_xlabel("Data Values")  # X label
                canvas = FigureCanvasTkAgg(fig, master=top_line_kdp)
                canvas.draw()
                canvas.get_tk_widget().pack()
            except Exception as err:
                print("KDP Error:", err)
                messagebox.showerror("KDP Plot Error",
                                     "Unable to plot the graph. Please try again with different data.")

    def scatterPlot(self, top_graph):
        dframe_hpr = helper_object_da.get_dframe()
        list_of_columns = list(self.listbox_graph_var.get(0, END))
        if len(list_of_columns) < 2:
            self.label_graph_error.configure(text="2 columns are required for graph. Please select 2 columns.",
                                             fg="red")
        elif len(list_of_columns) > 2:
            self.label_graph_error.configure(text="Please select maximum of 2 columns for scatter plot.",
                                             fg="red")
        else:
            self.label_graph_error.configure(text="")
            try:
                dfp = dframe_hpr[list_of_columns]
                if self.var_removeoutlierbeforeplot.get() == 1:
                    for cols in list_of_columns:
                        df_temp = helper_object_da.get_data_process_obj().get_1_5_IQR(dfp, cols)
                        dfp = df_temp
                top_line = tk.Toplevel(top_graph)
                top_line.attributes('-topmost', True)
                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                dfp.plot.scatter(x=list_of_columns[0], y=list_of_columns[1], ax=ax, title="Scatter Plot")
                canvas = FigureCanvasTkAgg(fig, master=top_line)
                canvas.draw()
                canvas.get_tk_widget().pack()
            except Exception as err:
                print("Scatter Plot Error:", err)
                messagebox.showerror("Scatter Plot Error",
                                     "Unable to plot the graph. Please try again with different data.")

    def pccMatrixGraph(self):
        if helper_object_da.get_dframe().empty:
            messagebox.showerror("Data Frame Empty",
                                 "The data frame is empty. Please select CSV file(s) and load it using the Load Data button.")
        else:
            corr = helper_object_da.get_dframe().corr(method='pearson')
            try:
                top_PCC_matrix = tk.Toplevel()
                top_PCC_matrix.title(configurable_constants.SW_TITLE + " - Correlation Matrix")
                top_PCC_matrix.attributes('-topmost', True)
                fig = Figure(figsize=(12, 9), dpi=100)
                ax = fig.add_subplot(111)
                heatmap = sns.heatmap(corr, cmap='RdYlGn_r', annot=True, linewidths=0.4, ax=ax, annot_kws={"size": 6}, )
                heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=90)
                heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0)
                heatmap.set_title('Correlation Matrix')
                canvas = FigureCanvasTkAgg(fig, master=top_PCC_matrix)
                canvas.draw()
                canvas.get_tk_widget().pack()
            except Exception as err:
                messagebox.showerror("PCC Matrix Plot Error",
                                     "Unable to plot the graph. Please try again with different data.")
