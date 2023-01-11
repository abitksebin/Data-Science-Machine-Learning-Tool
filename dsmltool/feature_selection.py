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
import os
import tkinter as tk
from tkinter import END, LEFT, RIGHT, X, Y, ACTIVE, messagebox

from scipy.stats.stats import pearsonr
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

from common_functions_helper import Helper

log = Helper.getInstance().get_logger()
helper_object_fs = Helper.getInstance()


class FeatureSelection:
    """Class that has all UI components and variables for Feature Selection Tab """

    def __init__(self, tab_feature_selection):
        self.tab_feature_selection = tab_feature_selection

        self.label_info_fewindow = tk.Label(self.tab_feature_selection, font='Helvetica 8 italic',
                                            text="Select target column and methods for doing feature extraction.",
                                            anchor="w")
        self.label_info_fewindow.pack(fill=X, pady=10, padx=20)
        self.frame_FE_sec1 = tk.Frame(self.tab_feature_selection, borderwidth=0, highlightthickness=0,
                                      highlightbackground="blue")
        self.frame_FE_sec1.pack()
        self.frame_FE_sec1_ls = tk.Frame(self.frame_FE_sec1, borderwidth=0, highlightthickness=0,
                                         highlightbackground="blue")
        self.frame_FE_sec1_ls.pack(side=LEFT)
        self.frame_FE_sec1_mid = tk.Frame(self.frame_FE_sec1, borderwidth=0, highlightthickness=0,
                                          highlightbackground="red")
        self.frame_FE_sec1_mid.pack(side=LEFT, padx=10)
        self.frame_FE_sec1_rs = tk.LabelFrame(self.frame_FE_sec1, borderwidth=1, highlightthickness=0,
                                              highlightbackground="red",
                                              text="Feature Extraction Methods")
        self.frame_FE_sec1_rs.pack(side=RIGHT, ipadx=20, ipady=5)
        self.label_FE_available_headers = tk.Label(self.frame_FE_sec1_ls, text="Available Columns")
        self.label_FE_available_headers.pack()
        self.scrollbar_FE_available_headers = tk.Scrollbar(self.frame_FE_sec1_ls)
        self.scrollbar_FE_available_headers.pack(side=RIGHT, fill=Y)
        self.listbox_FE_available_headers = tk.Listbox(self.frame_FE_sec1_ls, width=40, height=8,
                                                       yscrollcommand=self.scrollbar_FE_available_headers.set)
        self.listbox_FE_available_headers.pack()
        self.scrollbar_FE_available_headers.config(command=self.listbox_FE_available_headers.yview)
        self.listbox_FE_available_headers.delete(0, END)
        for col in helper_object_fs.get_dframe().columns:
            self.listbox_FE_available_headers.insert(END, col)

        self.frame_FE_target_var = tk.Frame(self.frame_FE_sec1_mid)
        self.frame_FE_target_var.pack()
        self.label_FE_target_var = tk.Label(self.frame_FE_target_var, text="Target Column:", font='Helvetica 9 bold')
        self.label_FE_target_var.pack(side=LEFT, pady=2)
        self.label_FE_target_var_selected = tk.Label(self.frame_FE_target_var, text="Not Selected",
                                                     font='Helvetica 9 bold')
        self.label_FE_target_var_selected.pack(side=LEFT)
        self.button_FE_addas_target = tk.Button(self.frame_FE_sec1_mid, text="Add selected column as target", height=1,
                                                width=25,
                                                command=self.addFETarget)
        self.button_FE_addas_target.pack(pady=2, padx=10)
        # self.button_FE_setas_category = tk.Button(self.frame_FE_sec1_mid, text="Change selected to category type", height=1, width=25,
        #                                   command= self.change_to_category_FS)
        # self.button_FE_setas_category.pack(pady=3, padx=10)
        self.var_FE_method_CA = tk.IntVar()
        self.var_FE_method_CA.set(0)
        self.checkbutton_var_FE_method_CA = tk.Checkbutton(self.frame_FE_sec1_rs, text="Correlation Based Method",
                                                           variable=self.var_FE_method_CA)
        self.checkbutton_var_FE_method_CA.pack(anchor="w", padx=20)
        self.frame_FE_sec1_rs_pcc = tk.Frame(self.frame_FE_sec1_rs)
        self.frame_FE_sec1_rs_pcc.pack(padx=30, fill=X)
        self.label_FE_pcc_cutoff = tk.Label(self.frame_FE_sec1_rs_pcc, text="PCC cut-off (+/-)")
        self.label_FE_pcc_cutoff.pack(side=LEFT, padx=10)
        self.entry_FE_pcc_cutoff = tk.Entry(self.frame_FE_sec1_rs_pcc, width=5)
        self.entry_FE_pcc_cutoff.insert(0, '0.3')
        self.entry_FE_pcc_cutoff.pack(side=LEFT)
        self.var_FE_method_ETC = tk.IntVar()
        self.var_FE_method_ETC.set(1)
        self.checkbutton_var_FE_method_ETC = tk.Checkbutton(self.frame_FE_sec1_rs,
                                                            text="Extra Trees Classifier Algorithm",
                                                            variable=self.var_FE_method_ETC)
        self.checkbutton_var_FE_method_ETC.pack(anchor="w", padx=20)
        self.frame_FE_sec1_rs_etc = tk.Frame(self.frame_FE_sec1_rs)
        self.frame_FE_sec1_rs_etc.pack(padx=35, fill=X)
        self.label_FE_etc_atr_number = tk.Label(self.frame_FE_sec1_rs_etc, text="Max number of features")
        self.label_FE_etc_atr_number.pack(side=LEFT)
        self.entry_FE_etc_atr_number = tk.Entry(self.frame_FE_sec1_rs_etc, width=5)
        self.entry_FE_etc_atr_number.insert(0, '3')
        self.entry_FE_etc_atr_number.pack(side=LEFT)
        self.var_FE_method_RFE = tk.IntVar()
        self.var_FE_method_RFE.set(0)
        self.checkbutton_var_FE_method_RFE = tk.Checkbutton(self.frame_FE_sec1_rs, text="Recursive Feature Elimination",
                                                            variable=self.var_FE_method_RFE)
        self.checkbutton_var_FE_method_RFE.pack(anchor="w", padx=20)
        self.frame_FE_sec1_rs_RFE = tk.Frame(self.frame_FE_sec1_rs)
        self.frame_FE_sec1_rs_RFE.pack(padx=35, fill=X)
        self.label_FE_RFE_atr_number = tk.Label(self.frame_FE_sec1_rs_RFE, text="Max number of features")
        self.label_FE_RFE_atr_number.pack(side=LEFT)
        self.entry_FE_RFE_atr_number = tk.Entry(self.frame_FE_sec1_rs_RFE, width=5)
        self.entry_FE_RFE_atr_number.insert(0, '3')
        self.entry_FE_RFE_atr_number.pack(side=LEFT)

        self.frame_FE_sec2 = tk.Frame(self.tab_feature_selection, borderwidth=0, highlightthickness=0,
                                      highlightbackground="green")
        self.frame_FE_sec2.pack(pady=2)
        self.button_FE_RA = tk.Button(self.frame_FE_sec1_mid, text="Run Feature Extraction",
                                      command=self.featureExtraction, height=2,
                                      width=35)
        self.button_FE_RA.pack(pady=5)
        self.frame_FE_sec2_save = tk.Frame(self.frame_FE_sec2, borderwidth=0, highlightthickness=0,
                                           highlightbackground="blue")
        self.frame_FE_sec2_save.pack(fill=X)
        self.label_FE_summary = tk.Label(self.frame_FE_sec2, text="Feature Extraction Summary:")
        self.label_FE_summary.pack()
        self.fe_file_export_req = tk.IntVar()
        self.cb_fe_file_save_required = tk.Checkbutton(self.frame_FE_sec1_mid, text="Save results to file",
                                                       variable=self.fe_file_export_req)
        self.cb_fe_file_save_required.pack(side=RIGHT, anchor='n')
        self.text_FE_op = tk.Text(self.frame_FE_sec2, height=20, width=120)
        self.text_FE_op.pack(padx=3, pady=2)
        self.label_FE_status = tk.Label(self.frame_FE_sec2, text="")
        self.label_FE_status.pack(pady=1)

        self.frame_FE_sec_finalise = tk.Frame(self.tab_feature_selection, borderwidth=0, highlightthickness=0,
                                              highlightbackground="white")
        self.frame_FE_sec_finalise.pack(pady=5, ipadx=5)

        self.frame_FE_sec_finalize_columns = tk.Frame(self.frame_FE_sec_finalise, borderwidth=0, highlightthickness=0,
                                                      highlightbackground="yellow")
        self.frame_FE_sec_finalize_columns.pack(side=LEFT)
        self.label_FE_finalize_fields = tk.Label(self.frame_FE_sec_finalize_columns, text="All Features")
        self.label_FE_finalize_fields.pack()
        self.scrollbar_FE_finalize_fields = tk.Scrollbar(self.frame_FE_sec_finalize_columns)
        self.scrollbar_FE_finalize_fields.pack(side=RIGHT, fill=Y)
        self.listbox_FE_finalize_fields = tk.Listbox(self.frame_FE_sec_finalize_columns, width=40, height=8,
                                                     yscrollcommand=self.scrollbar_FE_finalize_fields.set)
        self.listbox_FE_finalize_fields.pack()
        self.scrollbar_FE_finalize_fields.config(command=self.listbox_FE_finalize_fields.yview)

        self.frame_FE_sec_final_controls = tk.Frame(self.frame_FE_sec_finalise, borderwidth=0, highlightthickness=0,
                                                    highlightbackground="yellow")
        self.frame_FE_sec_final_controls.pack(side=LEFT, pady=5)

        self.btn_FE_add_selected = tk.Button(self.frame_FE_sec_final_controls, text="Add     >", height=1, width=15,
                                             command=self.add_column_to_selected_list)  # command = browsefunc
        self.btn_FE_add_selected.pack(pady=2)
        self.btn_FE_remove_selected = tk.Button(self.frame_FE_sec_final_controls, text="Remove  <", height=1, width=15,
                                                command=self.remove_column_from_selected_list)  # command = deleteFromItems
        self.btn_FE_remove_selected.pack(pady=2)
        self.btn_FE_add_all = tk.Button(self.frame_FE_sec_final_controls, text="Add all >>", height=1, width=15,
                                        command=self.add_all_columns_to_selected_list)  # command = new
        self.btn_FE_add_all.pack(pady=2)
        self.btn_FE_remove_all = tk.Button(self.frame_FE_sec_final_controls, text="Remove all <<", height=1, width=15,
                                           command=self.clear_selected_features_column)  # command = new
        self.btn_FE_remove_all.pack(pady=2)

        self.frame_FE_sec_selectedcolumns = tk.Frame(self.frame_FE_sec_finalise, borderwidth=0, highlightthickness=0,
                                                     highlightbackground="yellow")
        self.frame_FE_sec_selectedcolumns.pack(side=LEFT, pady=1)
        self.label_FE_selected_fields = tk.Label(self.frame_FE_sec_selectedcolumns, text="Selected Features")
        self.label_FE_selected_fields.pack()
        self.scrollbar_FE_selected_fields = tk.Scrollbar(self.frame_FE_sec_selectedcolumns)
        self.scrollbar_FE_selected_fields.pack(side=RIGHT, fill=Y)
        self.listbox_FE_selected_fields = tk.Listbox(self.frame_FE_sec_selectedcolumns, width=40, height=8,
                                                     yscrollcommand=self.scrollbar_FE_selected_fields.set)
        self.listbox_FE_selected_fields.pack()
        self.scrollbar_FE_selected_fields.config(command=self.listbox_FE_selected_fields.yview)
        # self.btn_FE_one_hot_encode = tk.Button(self.frame_FE_sec_finalise, text="Onehot Encode Category", height=1,
        #                                        width=20, command=self.onehot_encode_categories)
        # self.btn_FE_one_hot_encode.pack(pady=12)
        self.btn_FE_finalise_feature = tk.Button(self.frame_FE_sec_finalise, text="Confirm Features", height=2,
                                                 width=20, command=self.confirm_features)
        self.btn_FE_finalise_feature.pack(pady=2)
        self.selected_feature_in_listbox = []
        self.selected_target_column = None
        # self.listbox_FE_selected_fields.delete(0, END)
        # for col in helper_object_fs.get_dframe().columns:
        #     self.listbox_FE_selected_fields.insert(END, col)

    def add_column_to_selected_list(self):
        if (len(self.listbox_FE_finalize_fields.curselection()) > 0):
            currentitem = self.listbox_FE_finalize_fields.get(ACTIVE)
            if not currentitem in self.selected_feature_in_listbox:
                self.selected_feature_in_listbox.append(currentitem)
                self.listbox_FE_selected_fields.insert(END, currentitem)
        else:
            messagebox.showwarning("No columns selected", "No columns selected for adding to list.")

    def add_all_columns_to_selected_list(self):
        for item in self.listbox_FE_finalize_fields.get(0, END):
            if not item in self.selected_feature_in_listbox:
                self.selected_feature_in_listbox.append(item)
                self.listbox_FE_selected_fields.insert(END, item)

    def remove_column_from_selected_list(self):
        if (len(self.listbox_FE_selected_fields.curselection()) > 0):
            currentremitem = self.listbox_FE_selected_fields.get(ACTIVE)
            if currentremitem in self.selected_feature_in_listbox:
                self.selected_feature_in_listbox.remove(currentremitem)
            self.listbox_FE_selected_fields.delete(self.listbox_FE_selected_fields.curselection())
        else:
            messagebox.showwarning("No columns selected", "No columns selected for removing to list.")

    def update_column_list_in_ctrl(self):
        self.listbox_FE_available_headers.delete(0, END)
        self.listbox_FE_finalize_fields.delete(0, END)
        for col in helper_object_fs.get_dframe().columns:
            self.listbox_FE_available_headers.insert(END, col)
            self.listbox_FE_finalize_fields.insert(END, col)

    def addFETarget(self):
        if (len(self.listbox_FE_available_headers.curselection()) > 0):
            currentitem = self.listbox_FE_available_headers.get(ACTIVE)
            self.label_FE_status.configure(text="")
            self.label_FE_target_var_selected.configure(text=currentitem)
            self.selected_target_column = currentitem
        else:
            self.label_FE_status.configure(
                text="No items selected. Please select a value from the list of available columns.",
                fg="red")

    def correlation_FE(self, target, corr_limit):
        dframe = helper_object_fs.get_dframe()
        featurelistCA = []
        pcc_dic = {}
        df_target = dframe[target]
        df_feature = dframe.drop(target, axis=1)
        for var in df_feature.columns:
            pcc_dic[var] = round(pearsonr(df_target, df_feature[var])[0], 2)
        sort_dic = sorted(pcc_dic.items(), key=lambda x: x[1], reverse=True)
        string = "Correlation Based Method\n" + "-" * 50 + '\nFeatures with correlation coefficient with target >= ' + str(
            corr_limit) + ' & <=.98 (-ve & +ve)\n\n'
        for val in sort_dic:
            if abs(val[1]) >= corr_limit and abs(val[1]) <= .98:
                string = string + str(val[0]) + '   (' + str(val[1]) + ')\n'
                featurelistCA.append(val[0])
        string = string + '\n'
        return string, featurelistCA

    def ETC_FE(self, target, feature_limit):
        dframe = helper_object_fs.get_dframe()
        featurelist_ETC = []
        dframe.fillna(0, inplace=True)
        df_target = dframe[target]
        df_feature = dframe.drop(target, axis=1)
        X = df_feature.values
        Y = df_target.values
        model = ExtraTreesClassifier()
        model.fit(X, Y)
        feature_imp = model.feature_importances_
        res = zip(feature_imp, df_feature.columns)
        etc_dic = {}
        for elements in res:
            etc_dic[elements[1]] = elements[0]
        sort_dic = sorted(etc_dic.items(), key=lambda x: x[1], reverse=True)
        i = 1
        string = "Extra Tree Classifier Method\n" + "-" * 50 + '\nTop ' + str(
            feature_limit) + ' features ranked by feature importance : \n'
        for el in sort_dic:
            ln = str(i) + '  ' + str(el[0]) + '  (' + str(round(el[1], 3)) + ')'
            if i <= feature_limit:
                string = string + '\n' + ln
                featurelist_ETC.append(el[0])
            i = i + 1
        string = string + '\n'
        return string, featurelist_ETC

    def RFE_FE(self, target, feature_limit):
        dframe = helper_object_fs.get_dframe()
        string = "\nRecursive Feature Elimination Method\n" + "-" * 50 + '\nBest ' + str(
            feature_limit) + ' features: \n'
        featurelist_RFE = []
        dframe.fillna(0, inplace=True)
        df_target = dframe[target]
        df_feature = dframe.drop(target, axis=1)
        X = df_feature.values
        Y = df_target.values
        model = LogisticRegression()
        # create the RFE model and select 3 attributes
        rfe = RFE(model, n_features_to_select=feature_limit, step=1)
        rfe = rfe.fit(X, Y)
        # summarize the selection of the attributes
        bin_res = rfe.support_
        rank = rfe.ranking_
        dic = {}
        i = 0
        head_list = df_feature.columns
        for cols in bin_res:
            if cols:
                featurelist_RFE.append(head_list[i])
                dic[head_list[i]] = rank[i]
            i = i + 1
        for elements in featurelist_RFE:
            string = string + '\n' + (elements)
        return string, featurelist_RFE

    def listBestFeatures(self, featurelistCA, featurelistETC, featurelistRFE):
        selected_feature_list = []
        nonempty = 0
        string = ""
        f_dic = {}
        if featurelistCA:
            nonempty = nonempty + 1
        if featurelistETC:
            nonempty = nonempty + 1
        if featurelistRFE:
            nonempty = nonempty + 1
        if nonempty < 1:
            string = "No features extracted"
        else:
            comb_list = featurelistCA + featurelistETC + featurelistRFE
            for vals in (set(comb_list)):
                f_dic[vals] = comb_list.count(vals)
            sort_f_dic = sorted(f_dic.items(), key=lambda x: x[1], reverse=True)
            for features in sort_f_dic:
                if nonempty == 1:
                    string = string + str(features[0]) + '\n'
                    selected_feature_list.append(features[0])
                elif nonempty >= 2:
                    if features[1] >= 2:
                        selected_feature_list.append(features[0])
                        string = string + str(features[0]) + '\n'
            if nonempty == 1:
                string = '\nExtracted Features:\n' + '-' * 50 + '\n' + string
            if nonempty >= 2:
                string = '\nExtracted Features:\n' + '-' * 50 + '\n(Features common in at least 2 feature extraction methods)\n\n' + string
            string = string + '\n'
        return string, selected_feature_list

    def featureExtraction(self):
        dframe = helper_object_fs.get_dframe()
        target = self.label_FE_target_var_selected.cget("text")
        featurelistCA = []
        featurelistETC = []
        featurelistRFE = []
        fe_list = []
        FE_done = False
        fe_res_string = '*' * 15 + " Results from each method " + '*' * 15 + '\n'
        if self.var_FE_method_CA.get() == 0 and self.var_FE_method_ETC.get() == 0 and self.var_FE_method_RFE.get() == 0:
            self.label_FE_status.configure(text="Please select atleast one method for feature extraction.", fg="red")
        elif target == 'Not Selected':
            self.label_FE_status.configure(text="Please select a target column.", fg="red")
        else:
            self.label_FE_status.configure(text="", fg="red")
            CFE_results = ""
            total_featuresnumber = len(dframe.columns) - 1

            if self.var_FE_method_CA.get() == 1:
                try:
                    PCC_cutoff = self.entry_FE_pcc_cutoff.get()
                    if PCC_cutoff == "":
                        self.label_FE_status.configure(text="Please select a value between 0 and 1 for PCC cut-off.",
                                                       fg="red")
                    else:
                        floatPCC_cutoff = float(PCC_cutoff)
                        if floatPCC_cutoff < 0 or floatPCC_cutoff > 1:
                            self.label_FE_status.configure(
                                text="Please select a value between 0 and 1 for PCC cut-off.",
                                fg="red")
                        else:
                            self.label_FE_status.configure(text="", fg="red")
                            CFE_results, featurelistCA = self.correlation_FE(target, floatPCC_cutoff)
                            FE_done = True
                            fe_res_string = fe_res_string + '\n' + CFE_results
                except Exception as err:
                    # print (err)
                    self.label_FE_status.configure(text=str(err), fg="red")

            if self.var_FE_method_ETC.get() == 1:
                try:
                    ETC_limit = self.entry_FE_etc_atr_number.get()
                    intETC_limit = int(ETC_limit)
                    if ETC_limit == "":
                        self.label_FE_status.configure(
                            text="ETC:Please select a number between 1 and total number of features for consideration.",
                            fg="red")
                    else:
                        if intETC_limit < 0 or intETC_limit > total_featuresnumber:
                            self.label_FE_status.configure(
                                text=f"ETC:Please select a number between 1 and total number of features for consideration.",
                                fg="red")
                        else:
                            self.label_FE_status.configure(text="", fg="red")
                            ETC_results, featurelistETC = self.ETC_FE(target, intETC_limit)

                            FE_done = True
                            fe_res_string = fe_res_string + '\n' + ETC_results
                except Exception as err:
                    self.label_FE_status.configure(text=str(err), fg="red")
            if self.var_FE_method_RFE.get() == 1:
                try:
                    RFE_limit = self.entry_FE_RFE_atr_number.get()
                    intRFE_limit = int(RFE_limit)
                    if RFE_limit == "":
                        self.label_FE_status.configure(
                            text="RFE:Please select a number between 1 and total number of features for consideration.",
                            fg="red")
                    else:
                        if intRFE_limit < 0 or intRFE_limit > total_featuresnumber - 1:
                            self.label_FE_status.configure(
                                text="RFE:Please select a number between 1 and total number of features for consideration.",
                                fg="red")
                        else:
                            self.label_FE_status.configure(text="", fg="red")
                            RFE_results, featurelistRFE = self.RFE_FE(target, intRFE_limit)
                            FE_done = True
                            fe_res_string = fe_res_string + '\n' + RFE_results
                except Exception as err:
                    self.label_FE_status.configure(text=str(err), fg="red")
            if FE_done:
                fe_final_results, fe_list = self.listBestFeatures(featurelistCA, featurelistETC, featurelistRFE)
                FE_result = fe_final_results + '\n' + fe_res_string
                self.text_FE_op.delete('1.0', END)
                self.text_FE_op.insert(END, FE_result)
                if self.fe_file_export_req.get() == 1:
                    fe_results_file_name = os.path.join(
                        helper_object_fs.get_data_process_obj().label_exportpath_value.cget("text"),
                        helper_object_fs.get_data_process_obj().entry_output_path.get() + '_FeatureExtraction.txt')  # entry_output_path.get().replace('.csv','_')+'_PCC_results.txt'

                    helper_object_fs.ensure_dir(fe_results_file_name)
                    # print (FE_result)
                    file = open(fe_results_file_name, "a")
                    file.write(FE_result)
                    file.close()
                    self.label_FE_status.configure(text="Results are captured in file: " + str(fe_results_file_name),
                                                   fg="black")
                else:
                    self.label_FE_status.configure(text="")
        self.listbox_FE_selected_fields.delete(0, END)
        self.selected_feature_in_listbox.clear()
        for feature_items in fe_list:
            self.selected_feature_in_listbox.append(feature_items)
            self.listbox_FE_selected_fields.insert(END, feature_items)

    def clear_selected_features_column(self):
        self.listbox_FE_selected_fields.delete(0, END)
        self.selected_feature_in_listbox.clear()

    def confirm_features(self):
        helper_object_fs.set_selected_features_list(self.selected_feature_in_listbox)
        helper_object_fs.label_footer_df_status.configure(
            text=f"{len(self.selected_feature_in_listbox)} features selected for ML")
        helper_object_fs.set_selected_target_column(self.selected_target_column)
        helper_object_fs.populate_confirmed_feature_columns_in_tabs()
