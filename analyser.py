import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import pandas as pd
import numpy as np
from openpyxl import load_workbook

from utility import *


class analyser:

    def __init__(self, root, info):
        self.root = root
        self.information = info
        root.withdraw()
        self.data = pd.read_csv(self.information['pred_path'])
        self.master = tk.Tk()
        self.fig_frame = tk.Frame(self.master)
        self.master.wm_title("Graph.!")
        # self.master.tk.call('wm', 'iconphoto', self.master._w, tk.PhotoImage(file='HR_ICON.png'))

        plt.style.use("ggplot")
        if self.information['work_type'] == "DMS":
            self.collect_info_dms()

        else:
            # messagebox.askokcancel("Alert", "Functionality to Be built for Collections")
            self.distribute_cls()
            # root.deiconify()
            # self.master.protocol("WM_DELETE_WINDOW", self.close)
            # self.master.destroy()

        self.master.mainloop()

    def distribute_cls(self):
        self.data["Label"] = np.nan
        self.data["Label"] = np.where(
            (abs(self.data[self.information['predicted_key']] - self.data[self.information['actual_key']]) >= 10),
            "More than equal to 10", self.data["Label"])
        self.data["Label"] = np.where(
            (abs(self.data[self.information['predicted_key']] - self.data[self.information['actual_key']]) < 10),
            "within 5-10", self.data["Label"])
        self.data["Label"] = np.where(
            (abs(self.data[self.information['predicted_key']] - self.data[self.information['actual_key']]) < 5),
            "within 3-5", self.data["Label"])
        self.data["Label"] = np.where(
            (abs(self.data[self.information['predicted_key']] - self.data[self.information['actual_key']]) < 3),
            "within 1-3", self.data["Label"])
        self.data["Label"] = np.where(
            (abs(self.data[self.information['predicted_key']] - self.data[self.information['actual_key']]) < 1),
            "within 0-1", self.data["Label"])

        self.more_than_10_days = self.data[self.data['Label'] == "More than equal to 10"]
        self.within_10_days = self.data[self.data['Label'] == "within 5-10"]
        self.within_5_days = self.data[self.data['Label'] == "within 3-5"]
        self.within_3_days = self.data[self.data['Label'] == "within 1-3"]
        self.within_1_days = self.data[self.data['Label'] == "within 0-1"]

        if "excell_path" not in self.information.keys():
            self.information['excell_path'] = os.path.join(os.path.join(self.information['master_path'], "Analysed"),
                                                       "Classified.xlsx")
        dump_data("excell_path", self.information['excell_path'], self.information)

        writer = pd.ExcelWriter(self.information["excell_path"], engine="openpyxl")

        self.data.to_excel(writer, sheet_name='Predictions', index=False)
        self.within_1_days.to_excel(writer, sheet_name='Within 0-1', index=False)
        self.within_3_days.to_excel(writer, sheet_name='Within 1-3', index=False)
        self.within_5_days.to_excel(writer, sheet_name='Within 3-5', index=False)
        self.within_10_days.to_excel(writer, sheet_name='Within 5-10', index=False)
        self.more_than_10_days.to_excel(writer, sheet_name='More than equal to 10', index=False)

        writer.save()
        writer.close()

        self.CLS()

    def collect_info_dms(self):

        def is_float(val):
            try:
                float(val)
                return True
            except:
                print(val)
                return False

        def set_values():
            if auto_clear_threshold.get() == "" or spot_review_threshold.get() == "" or validity_threshold.get() == ""\
                or amt_auto_clear_threshold.get() == ""  or inv_amt_spot_review_threshold.get() == "" \
                    or v_amt_spot_review_threshold.get() == "":
                messagebox.askokcancel("Alert", "Seems some text are Empty Hmmmmm......!!!")
                return
            if not (is_float(auto_clear_threshold.get()) and is_float(spot_review_threshold.get()) \
                    and is_float(validity_threshold.get())\
                and is_float(amt_auto_clear_threshold.get()) and is_float(inv_amt_spot_review_threshold.get()) \
                    and is_float(v_amt_spot_review_threshold.get())):
                messagebox.askokcancel("Alert", "Seems some value is not numeric hmmm......!!!")
                return

            self.information['auto_clear_threshold'] = float(auto_clear_threshold.get())
            self.information['spot_review_threshold'] = float(spot_review_threshold.get())
            self.information['validity_threshold'] = float(validity_threshold.get())
            self.information['amt_auto_clear_threshold'] = float(amt_auto_clear_threshold.get())
            self.information['inv_amt_spot_review_threshold'] = float(inv_amt_spot_review_threshold.get())
            self.information['v_amt_spot_review_threshold'] = float(v_amt_spot_review_threshold.get())
            # self.master.deiconify()
            root.destroy()
            self.distribute_dms()


        self.master.withdraw()
        root = tk.Tk()
        pop_frame = tk.LabelFrame(root, text="Thresholds")
        #
        tk.Label(pop_frame, text="Auto-clear Threshold : ").grid(padx=5, pady=5)
        tk.Label(pop_frame, text="Spot-Review Treshold : ").grid(padx=5, pady=5)
        tk.Label(pop_frame, text="Validity Threshold : ").grid(padx=5, pady=5)
        tk.Label(pop_frame, text="Amt Treshold for Autoclear : ").grid(padx=5, pady=5)
        tk.Label(pop_frame, text="Invalid Amount Threshold for Spot Review : ").grid(padx=5, pady=5)
        tk.Label(pop_frame, text="Valid Amount Threshold for Spot Review: ").grid(padx=5, pady=5)
        #
        auto_clear_threshold = tk.Entry(pop_frame, width=20)
        spot_review_threshold = tk.Entry(pop_frame, width=20)
        validity_threshold = tk.Entry(pop_frame, width=20)
        amt_auto_clear_threshold = tk.Entry(pop_frame, width=20)
        inv_amt_spot_review_threshold = tk.Entry(pop_frame, width=20)
        v_amt_spot_review_threshold = tk.Entry(pop_frame, width=20)

        auto_clear_threshold.grid(row=0, column=1, padx=5, pady=5)
        spot_review_threshold.grid(row=1, column=1, padx=5, pady=5)
        validity_threshold.grid(row=2, column=1, padx=5, pady=5)
        amt_auto_clear_threshold.grid(row=3, column=1, padx=5, pady=5)
        inv_amt_spot_review_threshold.grid(row=4, column=1, padx=5, pady=5)
        v_amt_spot_review_threshold.grid(row=5, column=1, padx=5, pady=5)

        set_val(auto_clear_threshold, "0.9")
        set_val(spot_review_threshold, "0.8")
        set_val(validity_threshold, "0.5")
        set_val(amt_auto_clear_threshold, "500")
        set_val(inv_amt_spot_review_threshold, "2500")
        set_val(v_amt_spot_review_threshold, "10000")

        submit = tk.Button(pop_frame, text="Sure", command=set_values)
        submit.grid(column=1, padx=5,pady=5)
        pop_frame.grid(padx=5, pady=5)

        root.mainloop()

    def distribute_dms(self):
        self.data['Label'] = np.nan
        self.data['Label'] = \
            np.where((self.data['probability(1)'] < self.information['validity_threshold']) &
                    (self.data[self.information['amount_key']] <= self.information['inv_amt_spot_review_threshold']),
                     "spot_review_invalid", self.data['Label'])

        self.data['Label'] = np.where((
                ((self.data['probability(1)']>=self.information['spot_review_threshold'])&
                 (self.data[self.information['amount_key']]<self.information['v_amt_spot_review_threshold'])
        &(~((self.data['probability(1)']>=self.information['auto_clear_threshold'])&
            (self.data[self.information['amount_key']]<=self.information['amt_auto_clear_threshold']))))|
       ((self.data['probability(1)']>=self.information['validity_threshold'])&
        (self.data['probability(1)']<self.information['spot_review_threshold'])&
        (self.data[self.information['amount_key']]<self.information['inv_amt_spot_review_threshold']))),
            "spot_review_valid", self.data['Label'])

        self.data['Label'] = \
            np.where(((self.data['probability(1)']>=self.information['auto_clear_threshold'])&
                    (self.data[self.information['amount_key']]<=self.information['amt_auto_clear_threshold'])),
                                       "auto_clear_valid", self.data['Label'])

        self.data['Label'] = np.where(((self.data['probability(1)'] >=self.information['validity_threshold']) &
        (~(((self.data['probability(1)']>=self.information['spot_review_threshold'])&
            (self.data[self.information['amount_key']]<self.information['v_amt_spot_review_threshold']))|
           ((self.data['probability(1)']>=self.information['validity_threshold'])&
            (self.data['probability(1)']<self.information['spot_review_threshold'])&
            (self.data[self.information['amount_key']]<self.information['inv_amt_spot_review_threshold'])))))|
        ((self.data['probability(1)']<self.information['validity_threshold']) &
         (self.data[self.information['amount_key']]>self.information['inv_amt_spot_review_threshold'])),
                                      "further_research", self.data['Label'])

        self.data['can_be_autocleared'] = np.where(
            (self.data[self.information['amount_key']] < self.information['amt_auto_clear_threshold']) &
            (self.data[self.information['actual_key']] == 1), "Can Be AutoCleared", "Can-not be AutoCleared"
        )

        self.spot_review_invalid = self.data[self.data.Label == "spot_review_invalid"]
        self.spot_review_valid = self.data[self.data.Label == "spot_review_valid"]
        self.auto_clear_valid = self.data[self.data.Label == "auto_clear_valid"]
        self.further_research = self.data[self.data.Label == "further_research"]

        if "excell_path" not in self.information.keys():
            self.information['excell_path'] = os.path.join(os.path.join(self.information['master_path'], "Analysed"),
                                                       "Classified.xlsx")
        dump_data("excell_path", self.information['excell_path'], self.information)

        writer = pd.ExcelWriter(self.information["excell_path"], engine="openpyxl")

        self.data.to_excel(writer, sheet_name='Predictions', index=False)
        self.auto_clear_valid.to_excel(writer, sheet_name='Auto_Clear_Valid', index=False)
        self.spot_review_valid.to_excel(writer, sheet_name='Spot_Eeview_Valid', index=False)
        self.spot_review_invalid.to_excel(writer, sheet_name='Spot_Review_Invalid', index=False)
        self.further_research.to_excel(writer, sheet_name='Further_Research', index=False)

        writer.save()
        writer.close()

        solver = load_workbook(os.path.join(os.path.join(os.getcwd(), "Solver"), "Solver.xlsx"))
        solver_sheet = solver['Solver']
        solver_sheet['B1'].value = self.information['auto_clear_threshold']
        solver_sheet['B2'].value = self.information['spot_review_threshold']
        solver_sheet['B3'].value = self.information['validity_threshold']
        solver_sheet['B4'].value = self.information['amt_auto_clear_threshold']
        solver_sheet['B5'].value = self.information['inv_amt_spot_review_threshold']
        solver_sheet['B6'].value = self.information['v_amt_spot_review_threshold']

        if "solver_path" not in self.information.keys():
            self.information['solver_path'] = os.path.join(os.path.join(self.information['master_path'], "Analysed"),
                                                       self.information['account_name'] + "Solver.xlsx")
        dump_data("solver_path", self.information['solver_path'], self.information)

        writer = pd.ExcelWriter(self.information["solver_path"], engine="openpyxl")
        writer.book = solver
        writer.sheets = dict((ws.title, ws) for ws in solver.worksheets)

        self.data[[self.information["amount_key"], "primaryKey",
                   "probability(1)",
                   self.information["actual_key"]]].to_excel(writer, sheet_name="Entry",
                                                             index=False, startrow=0, startcol=2, header=None)

        writer.save()
        writer.close()
        self.DMS()



    def close(self):
        quit()

    def DMS(self):
        fig = plt.figure()


        a1 = plt.subplot2grid((9, 9), (0, 0), rowspan=3, colspan=3)

        self.data.Label.value_counts().plot.pie(autopct="%1.1f%%", shadow=True, colors=sns.color_palette('Set3', 10),
                                                startangle=90, wedgeprops={'linewidth':2, 'edgecolor':'white'}, ax=a1,
                                                explode=[0, 0, 0.2, 0])
        my_circle = plt.Circle((0, 0), 0.4, color="white")
        plt.ylabel("")
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        a2 = plt.subplot2grid((9, 9), (0, 3), rowspan=3, colspan=3)

        self.data.can_be_autocleared.value_counts().plot.pie(autopct="%1.1f%%", shadow=True,
                                                             colors=sns.color_palette('Set3', 5),
                                                startangle=90, wedgeprops={'linewidth':2, 'edgecolor':'white'}, ax=a2,
                                                             explode=[0, 0.1])
        my_circle = plt.Circle((0, 0), 0.4, color="white")
        plt.ylabel("")
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        a3 = plt.subplot2grid((9, 9), (0, 7), rowspan=3, colspan=3)

        self.data.groupby([self.information['actual_key'],
                           self.information['predicted_key']])["primaryKey"].count().plot.barh(
            width=0.9, color=sns.color_palette('RdYlGn', 10), ax=a3
        )

        a4 = plt.subplot2grid((9, 9), (4, 0), rowspan=3, colspan=9)

        self.data.groupby([self.information['actual_key'],
                           self.information['predicted_key']])[self.information["amount_key"]].agg("sum").plot.bar(
            width=0.9, color=sns.color_palette('RdYlGn', 10), ax=a4
        )

        a5 = plt.subplot2grid((9, 9), (8, 0), rowspan=2, colspan=9)

        sns.distplot(self.data['probability(1)'], ax=a5)
        # plt.ylabel("probability Valid")

        canvas = FigureCanvasTkAgg(fig, self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.fig_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig_frame.pack(padx=5, pady=5, fill='both', expand=True)
        self.master.state("zoomed")
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.master.deiconify()


    def CLS(self):
        fig = plt.figure()

        a1 = plt.subplot2grid((5, 7), (0, 0), rowspan=3, colspan=3)

        self.data.Label.value_counts().plot.pie(autopct="%1.1f%%", shadow=True, colors=sns.color_palette('Set3', 10),
                                                startangle=90, wedgeprops={'linewidth':2, 'edgecolor':'white'}, ax=a1)
        my_circle = plt.Circle((0, 0), 0.4, color="white")
        plt.ylabel("")
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        a2 = plt.subplot2grid((7, 7), (0, 4), rowspan=3, colspan=3)

        self.data.Label.value_counts().plot.bar(color=sns.color_palette('Set3', 10), ax=a2)

        a3 = plt.subplot2grid((7, 7), (4, 0), rowspan=3, colspan=7)

        a3.plot(self.data[self.information['actual_key']], color='b', Label="Actual")
        a3.plot(self.data[self.information['predicted_key']], color='red', Label="predicted")
        a3.legend(loc="best")

        # a4 = plt.subplot2grid((9, 9), (4, 0), rowspan=3, colspan=9)
        #
        # self.data.groupby([self.information['actual_key'],
        #                    self.information['predicted_key']])[self.information["amount_key"]].agg("sum").plot.bar(
        #     width=0.9, color=sns.color_palette('RdYlGn', 10), ax=a4
        # )
        #
        # a5 = plt.subplot2grid((9, 9), (8, 0), rowspan=2, colspan=9)
        #
        # sns.distplot(self.data['probability(1)'], ax=a5)
        # plt.ylabel("probability Valid")

        canvas = FigureCanvasTkAgg(fig, self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.fig_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig_frame.pack(padx=5, pady=5, fill='both', expand=True)
        self.master.state("zoomed")
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.master.deiconify()


