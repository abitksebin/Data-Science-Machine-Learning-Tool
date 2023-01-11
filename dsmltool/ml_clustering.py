# -------------------------------------------------------------------------------
# Name:        ml_clustering.py
# Purpose:     ML Clustering Tab code of the tool
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
from tkinter import END, LEFT, RIGHT, X, Y, N, messagebox, filedialog
from tkinter import ttk

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

import configurable_constants
from common_functions_helper import Helper


class MlClusteringAlgorithms:
    KMEANS = "KMeans"
    DBSCAN = "DBSCAN"
    AGLOMERATIVE = "AgglomerativeClustering"


log = Helper.getInstance().get_logger()
helper_object_ml_clr = Helper.getInstance()


class MlClustering:
    """Class that has all UI components and variables for ML Training - Clustering Tab """

    def __init__(self, tab_ml_clustering):
        self.X = None
        self.clustering_model = None
        self.tab_ml_clustering = tab_ml_clustering
        self.label_info_ml_classification = tk.Label(self.tab_ml_clustering, font='Helvetica 8 italic',
                                                     text="Machine Learning - Clustering.",
                                                     anchor="w")
        self.label_info_ml_classification.pack(fill=X, pady=10, padx=20)

        self.frame_MLCLR_row1 = tk.Frame(self.tab_ml_clustering, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_MLCLR_row1.pack(fill=X, padx=3)

        self.frame_MLCLR_row1_available_columns = tk.Frame(self.frame_MLCLR_row1, borderwidth=0, highlightthickness=0,
                                                           highlightbackground="yellow")
        self.frame_MLCLR_row1_available_columns.pack(side=LEFT, pady=2)
        self.label_MLCLR_available_headers = tk.Label(self.frame_MLCLR_row1_available_columns, text="Filtered Columns")
        self.label_MLCLR_available_headers.pack()
        self.scrollbar_MLCLR_available_columns = tk.Scrollbar(self.frame_MLCLR_row1_available_columns)
        self.scrollbar_MLCLR_available_columns.pack(side=RIGHT, fill=Y)
        self.listbox_MLCLR_available_columns = tk.Listbox(self.frame_MLCLR_row1_available_columns, width=40, height=7,
                                                          yscrollcommand=self.scrollbar_MLCLR_available_columns.set)
        self.listbox_MLCLR_available_columns.pack()
        self.scrollbar_MLCLR_available_columns.config(command=self.listbox_MLCLR_available_columns.yview)

        self.frame_MLCLR_row1_options_mid = tk.Frame(self.frame_MLCLR_row1, borderwidth=0, highlightthickness=0,
                                                     highlightbackground="yellow")
        self.frame_MLCLR_row1_options_mid.pack(side=LEFT, pady=2, padx=15, ipady=5)

        self.frame_MLCLR_target_var = tk.Frame(self.frame_MLCLR_row1_options_mid)
        self.frame_MLCLR_target_var.pack(fill=X)

        self.frame_MLCLR_row1_options_algorithms = tk.Frame(self.frame_MLCLR_row1_options_mid, borderwidth=0,
                                                            highlightthickness=0, highlightbackground="yellow")
        self.frame_MLCLR_row1_options_algorithms.pack(pady=20, ipady=3)
        self.label_MLCLR_algorithm = tk.Label(self.frame_MLCLR_row1_options_algorithms, text="Algorithm:")
        self.label_MLCLR_algorithm.pack(side=LEFT)

        self.var_MLCLR_algorithm = tk.StringVar()
        self.combobox_MLCLR_algorithm = ttk.Combobox(self.frame_MLCLR_row1_options_algorithms,
                                                     textvariable=self.var_MLCLR_algorithm,
                                                     values=[MlClusteringAlgorithms.KMEANS,
                                                             MlClusteringAlgorithms.DBSCAN,
                                                             MlClusteringAlgorithms.AGLOMERATIVE
                                                             ], state="readonly")
        self.combobox_MLCLR_algorithm.current(0)
        self.combobox_MLCLR_algorithm.pack(side=LEFT)

        self.frame_MLCLR_row1_options_parent = tk.Frame(self.frame_MLCLR_row1)
        self.frame_MLCLR_row1_options_parent.pack(side=LEFT, pady=2, padx=20)

        self.frame_MLCLR_row1_options = tk.LabelFrame(self.frame_MLCLR_row1_options_parent, text="Options")
        self.frame_MLCLR_row1_options.pack(pady=2, padx=20)

        self.frame_MLCLR_row1_options_kmeans = tk.LabelFrame(self.frame_MLCLR_row1_options,
                                                             text="K-Means | Aglomerative", width=50)
        self.frame_MLCLR_row1_options_kmeans.pack(pady=2, ipadx=2, padx=6, side=LEFT)

        self.frame_MLCLR_kmeans_n = tk.Frame(self.frame_MLCLR_row1_options_kmeans)
        self.frame_MLCLR_kmeans_n.pack(fill=X, ipadx=5, ipady=3)
        self.label_MLCLR_kmeans_n = tk.Label(self.frame_MLCLR_kmeans_n, text="Number of clusters")
        self.label_MLCLR_kmeans_n.pack(side=LEFT, padx=5)
        self.entry_MLCLR_kmeans_n = tk.Entry(self.frame_MLCLR_kmeans_n, width=5)
        self.entry_MLCLR_kmeans_n.insert(0, '3')
        self.entry_MLCLR_kmeans_n.pack(side=LEFT)

        self.frame_MLCLR_row1_options_dbscan = tk.LabelFrame(self.frame_MLCLR_row1_options, text="DBSCAN")
        self.frame_MLCLR_row1_options_dbscan.pack(pady=2, ipadx=2, padx=6, side=LEFT)

        self.frame_MLCLR_dbscan_min_samples = tk.Frame(self.frame_MLCLR_row1_options_dbscan)
        self.frame_MLCLR_dbscan_min_samples.pack(fill=X, ipadx=5, ipady=3)
        self.label_MLCLR_dbscan_min_samples = tk.Label(self.frame_MLCLR_dbscan_min_samples, text="Min_samples")
        self.label_MLCLR_dbscan_min_samples.pack(side=LEFT, padx=5)
        self.entry_MLCLR_dbscan_min_samples = tk.Entry(self.frame_MLCLR_dbscan_min_samples, width=5)
        self.entry_MLCLR_dbscan_min_samples.insert(0, '3')
        self.entry_MLCLR_dbscan_min_samples.pack(side=LEFT)

        self.frame_MLCLR_dbscan_eps = tk.Frame(self.frame_MLCLR_row1_options_dbscan)
        self.frame_MLCLR_dbscan_eps.pack(fill=X, ipadx=5, ipady=3)
        self.label_MLCLR_dbscan_eps = tk.Label(self.frame_MLCLR_dbscan_eps, text="EPS (min. dist. b/w samples)")
        self.label_MLCLR_dbscan_eps.pack(side=LEFT, padx=5)
        self.entry_MLCLR_dbscan_eps = tk.Entry(self.frame_MLCLR_dbscan_eps, width=5)
        self.entry_MLCLR_dbscan_eps.insert(0, '0.5')
        self.entry_MLCLR_dbscan_eps.pack(side=LEFT)
        self.var_MLCLR_options_scale = tk.IntVar()
        self.var_MLCLR_options_scale.set(1)
        self.checkbutton_MLCLR_options_scale = tk.Checkbutton(self.frame_MLCLR_row1_options,
                                                              text="Scale Data (Standard Scaler)",
                                                              variable=self.var_MLCLR_options_scale)
        self.checkbutton_MLCLR_options_scale.pack(anchor=N, padx=5)
        self.button_MLCLR_elbow_test = tk.Button(self.frame_MLCLR_row1_options_kmeans, text="Elbow Test (KMeans)",
                                                 command=self.run_elbow_test, height=1, width=20)
        self.button_MLCLR_elbow_test.pack(pady=10)

        self.button_MLCLR_train_model = tk.Button(self.frame_MLCLR_row1_options_mid, text="Start Clustering",
                                                  command=self.start_MCLR_training, height=2, width=30)
        self.button_MLCLR_train_model.pack(pady=10)

        self.frame_MLCLR_row2 = tk.Frame(self.tab_ml_clustering, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_MLCLR_row2.pack(fill=X, padx=3)

        label_MLCLR_train_test_split_heading = tk.Label(self.frame_MLCLR_row2,
                                                        text="Results").pack()
        self.text_MLCLR_train_results = tk.Text(self.frame_MLCLR_row2, height=20, width=120)
        self.text_MLCLR_train_results.pack(padx=3, pady=2)

        self.clustering_model = None
        self.cluster_labels = None

        self.frame_MLCLR_row3 = tk.Frame(self.tab_ml_clustering, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_MLCLR_row3.pack(fill=X, padx=10, pady=15, ipady=5)
        self.button_MLCLR_export_clustered_data_nonscaled = tk.Button(self.frame_MLCLR_row3,
                                                                      text="Export Clustered Data (Non-Scaled)",
                                                                      height=2, width=28,
                                                                      command=self.export_clustered_data)
        self.button_MLCLR_export_clustered_data_nonscaled.pack(side=LEFT, padx=10, ipady=5)
        self.button_MLCLR_export_clustered_data_scaled = tk.Button(self.frame_MLCLR_row3,
                                                                   text="Export Clustered Data (Scaled)",
                                                                   height=2, width=28,
                                                                   command=self.export_clustered_data_scaled)
        self.button_MLCLR_export_clustered_data_scaled.pack(side=LEFT, padx=10, ipady=5)

        self.button_MLCLR_plot_cluster_data = tk.Button(self.frame_MLCLR_row3,
                                                        text="Plot Clustered Data",
                                                        height=2,
                                                        width=28, command=self.plot_clustered_data)
        self.button_MLCLR_plot_cluster_data.pack(side=LEFT, padx=10, ipady=5)
        self.button_MLCLR_export_model = tk.Button(self.frame_MLCLR_row3, text="Export Model", height=2, width=28,
                                                   command=self.export_model)
        self.button_MLCLR_export_model.pack(side=LEFT, padx=10, ipady=5)

    def run_elbow_test(self):
        iner_list = []
        k_list = []
        df = helper_object_ml_clr.get_dframe()
        selected_features = helper_object_ml_clr.get_selected_features_list()
        self.X = df[selected_features]
        for i in range(1, 11):
            clustering = KMeans(n_clusters=i)
            clustering.fit(df)
            iner_list.append(clustering.inertia_)
            k_list.append(i)
        plt.plot(k_list, iner_list)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.legend()
        plt.show()

    def start_MCLR_training(self):
        df = helper_object_ml_clr.get_dframe()
        selected_features = helper_object_ml_clr.get_selected_features_list()
        if df is None or len(selected_features) == 0:
            messagebox.showerror("Error", "Please load data and confirm features before training.")
        else:
            try:
                self.X = df[selected_features]
                if self.var_MLCLR_options_scale.get() == 1:
                    self.X = StandardScaler().fit_transform(self.X)

                if self.var_MLCLR_algorithm.get() == MlClusteringAlgorithms.KMEANS:
                    self.clustering_model = KMeans(n_clusters=int(self.entry_MLCLR_kmeans_n.get()))
                elif self.var_MLCLR_algorithm.get() == MlClusteringAlgorithms.DBSCAN:
                    self.clustering_model = DBSCAN(eps=float(self.entry_MLCLR_dbscan_eps.get()),
                                                   min_samples=int(self.entry_MLCLR_dbscan_min_samples.get()))
                elif self.var_MLCLR_algorithm.get() == MlClusteringAlgorithms.AGLOMERATIVE:
                    self.clustering_model = AgglomerativeClustering(n_clusters=int(self.entry_MLCLR_kmeans_n.get()))
                self.text_MLCLR_train_results.insert(END,
                                                     f'\n>> Clustering started using the algorithm: {self.var_MLCLR_algorithm.get()} at {str(datetime.now())}.')
                self.clustering_trained_model = self.clustering_model.fit(self.X)

                self.cluster_labels = self.clustering_model.labels_
                silhouette_score_for_model = silhouette_score(self.X, self.cluster_labels, metric='euclidean')
                self.text_MLCLR_train_results.insert(END,
                                                     f'\n>> Clustering completed at {str(datetime.now())}. Please use "Export Results" button to export results.')
                self.text_MLCLR_train_results.insert(END,
                                                     f'\n>> Model Summary: {repr(self.clustering_trained_model)}.')
                self.text_MLCLR_train_results.insert(END,
                                                     f'\n>> Silhouette Score: {silhouette_score_for_model} \n')

                self.text_MLCLR_train_results.insert(END, '--' * 50)
                helper_object_ml_clr.update_bottom_status_bar('Clustering completed')

            except Exception as err:
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def plot_clustered_data(self):
        try:
            if self.clustering_model is None:
                messagebox.showerror("Model not trained", "The model is not trained. Please train before exporting.")
            else:
                u_labels = np.unique(self.cluster_labels)
                # plotting the results:
                for i in u_labels:
                    plt.scatter(self.X[self.cluster_labels == i, 0], self.X[self.cluster_labels == i, 1], label=i)
                plt.legend()
                plt.show()

        except Exception as err:
            messagebox.showerror("Error", f"Unable do the requested action.{err}")
            log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def export_model(self):
        if self.clustering_model is None:
            messagebox.showerror("Model not trained", "The model is not trained. Please train before exporting.")
        else:
            try:
                file_dialog = filedialog.asksaveasfile(mode='w',
                                                       defaultextension=f".{configurable_constants.MODEL_EXPORT_EXTENSION}")
                if file_dialog is None:
                    return
                pickle.dump(self.clustering_model, open(file_dialog.name, 'wb'))
                messagebox.showinfo("Exported", f"Model exported to the path : {file_dialog.name}")
            except Exception as err:
                messagebox.showerror("Error", "Unable to export model.")
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))

    def export_clustered_data(self):
        if self.clustering_model is None:
            messagebox.showerror("Model not trained", "The model is not trained. Please train before exporting.")
        else:
            try:
                file_dialog = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
                if file_dialog is None:
                    return
                df = helper_object_ml_clr.get_dframe()
                selected_features = helper_object_ml_clr.get_selected_features_list()
                non_scaled_data = df[selected_features]
                non_scaled_data["Cluster"] = self.cluster_labels
                non_scaled_data.to_csv(file_dialog.name)
                messagebox.showinfo("Exported", "Data exported")
            except Exception as err:
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))
                messagebox.showerror("Error", "Unable to export data.")

    def export_clustered_data_scaled(self):
        if self.clustering_model is None:
            messagebox.showerror("Model not trained", "The model is not trained. Please train before exporting.")
        else:
            try:
                file_dialog = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
                if file_dialog is None:
                    return
                df = pd.DataFrame(self.X, columns=helper_object_ml_clr.get_selected_features_list())
                df["Cluster"] = self.cluster_labels
                df.to_csv(file_dialog.name)
                messagebox.showinfo("Exported", "Data exported")
            except Exception as err:
                log.error(Helper.log_format(__name__, sys._getframe().f_code.co_name, err))
                messagebox.showerror("Error", "Unable to export data.")
