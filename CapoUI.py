from TextBox import *
from preprocessing import preprocessing
from aggregation import aggregation
from modeltrainer import modeltrainer
from modelpredictor import modelpredictor
from scoring import scoring
from utility import *
import os, pickle
from analyser import analyser

class controllerUI:
    '''
    This class is the master class responsible for all the events of related to UI
    '''
    def __init__(self):
        self.ui = ui()

    def run(self):
        self.ui.start_ui()


class ui:
    '''
    This class is the representation of UI of CaPo
    '''
    def __init__(self, normal_hitrate=100, execution_hitrate=1000):
        self.root = tk.Tk(className='CaPo')
        self.root.state('zoomed')
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='HR_ICON.png'))

        self.fileMenu = self.make_file_menu()
        self.normal_hitrate = normal_hitrate
        self.execution_hitrate = execution_hitrate

        self.pre_processing_textbox = preprocessing(self.root, row=0, col=0, label='preprocessing')
        self.aggregation_textbox = aggregation(self.root, row=1, col=0, label='aggregation')
        self.model_trainer_textbox = modeltrainer(self.root, row=0, col=1, label='model_generators')
        self.model_predictor_textbox = modelpredictor(self.root, row=1, col=1, label='model_predictors')
        self.info = {}
        self.fileMenu = self.make_file_menu()
        self.block_execute()

    # def reactive(self):
    #     self.pre_processing_textbox.execute_button['state'] = 'active'
    #     self.model_trainer_textbox.execute_button['state'] = 'active'
    #     self.aggregation_textbox.execute_button['state'] = 'active'
    #     self.model_predictor_textbox.execute_button['state'] = 'active'
    #
    #     self.pre_processing_textbox.pool = None
    #     self.aggregation_textbox.pool = None
    #     self.model_trainer_textbox.pool = None
    #     self.model_predictor_textbox.pool = None
    #     self.root.after(self.normal_hitrate, self.block_execute)

    # def block_execute(self):
    #
    #     if self.pre_processing_textbox.pool != None:
    #         if any(p.is_alive() for p in self.pre_processing_textbox.pool):
    #             self.aggregation_textbox.execute_button['state'] = 'disabled'
    #             self.model_trainer_textbox.execute_button['state'] = 'disabled'
    #             self.model_predictor_textbox.execute_button['state'] = 'disabled'
    #             self.root.after(self.execution_hitrate, self.block_execute)
    #         else:
    #             self.reactive()
    #
    #     elif self.aggregation_textbox.pool != None:
    #         if any(p.is_alive() for p in self.aggregation_textbox.pool):
    #             self.pre_processing_textbox.execute_button['state'] = 'disabled'
    #             self.model_trainer_textbox.execute_button['state'] = 'disabled'
    #             self.model_predictor_textbox.execute_button['state'] = 'disabled'
    #             self.root.after(self.execution_hitrate, self.block_execute)
    #         else:
    #             self.reactive()
    #
    #     elif self.model_trainer_textbox.pool != None:
    #         if any(p.is_alive() for p in self.model_trainer_textbox.pool):
    #             self.pre_processing_textbox.execute_button['state'] = 'disabled'
    #             self.aggregation_textbox.execute_button['state'] = 'disabled'
    #             self.model_predictor_textbox.execute_button['state'] = 'disabled'
    #             self.root.after(self.execution_hitrate, self.block_execute)
    #         else:
    #             self.reactive()
    #     elif self.model_predictor_textbox.pool != None:
    #         if any(p.is_alive() for p in self.model_predictor_textbox.pool):
    #             self.pre_processing_textbox.execute_button['state'] = 'disabled'
    #             self.model_trainer_textbox.execute_button['state'] = 'disabled'
    #             self.aggregation_textbox.execute_button['state'] = 'disabled'
    #             self.root.after(self.execution_hitrate, self.block_execute)
    #         else:
    #             self.reactive()
    #     else:
    #         self.root.after(self.normal_hitrate, self.block_execute)

    def reactive(self):
        self.pre_processing_textbox.execute_button['state'] = 'active'
        self.model_trainer_textbox.execute_button['state'] = 'active'
        self.aggregation_textbox.execute_button['state'] = 'active'
        self.model_predictor_textbox.execute_button['state'] = 'active'

        self.pre_processing_textbox.t1 = None
        self.aggregation_textbox.t1 = None
        self.model_trainer_textbox.t1 = None
        self.model_predictor_textbox.t1 = None
        self.root.after(self.normal_hitrate, self.block_execute)


    def block_execute(self):

        if self.pre_processing_textbox.t1 != None:
            if self.pre_processing_textbox.t1.isAlive():
                self.aggregation_textbox.execute_button['state'] = 'disabled'
                self.model_trainer_textbox.execute_button['state'] = 'disabled'
                self.model_predictor_textbox.execute_button['state'] = 'disabled'
                self.root.after(self.execution_hitrate, self.block_execute)
            else:
                self.pre_processing_textbox.show_message()
                self.reactive()

        elif self.aggregation_textbox.t1 != None:
            if self.aggregation_textbox.t1.isAlive():
                self.pre_processing_textbox.execute_button['state'] = 'disabled'
                self.model_trainer_textbox.execute_button['state'] = 'disabled'
                self.model_predictor_textbox.execute_button['state'] = 'disabled'
                self.root.after(self.execution_hitrate, self.block_execute)
            else:
                self.aggregation_textbox.show_message()
                self.reactive()

        elif self.model_trainer_textbox.t1 != None:
            if self.model_trainer_textbox.t1.isAlive():
                self.pre_processing_textbox.execute_button['state'] = 'disabled'
                self.aggregation_textbox.execute_button['state'] = 'disabled'
                self.model_predictor_textbox.execute_button['state'] = 'disabled'
                self.root.after(self.execution_hitrate, self.block_execute)
            else:
                self.model_trainer_textbox.show_message()
                self.reactive()
        elif self.model_predictor_textbox.t1 != None:
            if self.model_predictor_textbox.t1.isAlive():
                self.pre_processing_textbox.execute_button['state'] = 'disabled'
                self.model_trainer_textbox.execute_button['state'] = 'disabled'
                self.aggregation_textbox.execute_button['state'] = 'disabled'
                self.root.after(self.execution_hitrate, self.block_execute)
            else:
                self.model_predictor_textbox.show_message()
                self.reactive()
        else:
            self.root.after(self.normal_hitrate, self.block_execute)



    def initiate(self):
        self.info['master_path'] = os.path.join(self.info['working_directory'], self.info['account_name'])
        self.info['dump_path'] = os.path.join(os.getcwd(), os.path.join('Dump', self.info['account_name']))
        os.makedirs(self.info['master_path'], exist_ok=True)
        os.makedirs(os.path.join(self.info['master_path'], 'PreProcessed'), exist_ok=True)
        os.makedirs(os.path.join(self.info['master_path'], 'Aggregation'), exist_ok=True)
        os.makedirs(os.path.join(self.info['master_path'], 'Model'), exist_ok=True)
        os.makedirs(os.path.join(self.info['master_path'], 'Prediction'), exist_ok=True)
        os.makedirs(os.path.join(self.info['master_path'], 'Commands'), exist_ok=True)
        os.makedirs(os.path.join(self.info['master_path'], 'Analysed'), exist_ok=True)
        os.makedirs(self.info['dump_path'], exist_ok=True)
        file = open(os.path.join(self.info['dump_path'], self.info['account_name'] + '_info.pickle'), 'wb')
        pickle.dump(self.info, file)
        file.close()

    def fill_text(self):
        self.pre_processing_textbox.clear_textbox()
        self.aggregation_textbox.clear_textbox()
        self.model_trainer_textbox.clear_textbox()
        self.model_predictor_textbox.clear_textbox()
        if 'preprocess_cmd' in self.pre_processing_textbox.text_box_info.keys():
            self.pre_processing_textbox.textbox.insert(tk.INSERT,
                                                       self.pre_processing_textbox.text_box_info['preprocess_cmd'])

        if 'aggregation_cmd' in self.aggregation_textbox.text_box_info.keys():
            self.aggregation_textbox.textbox.insert(tk.INSERT,
                                                       self.aggregation_textbox.text_box_info['aggregation_cmd'])

        if 'model_cmd' in self.model_trainer_textbox.text_box_info.keys():
            self.model_trainer_textbox.textbox.insert(tk.INSERT,
                                                       self.model_trainer_textbox.text_box_info['model_cmd'])

        if 'prediction_cmd' in self.model_predictor_textbox.text_box_info.keys():
            self.model_predictor_textbox.textbox.insert(tk.INSERT,
                                                       self.model_predictor_textbox.text_box_info['prediction_cmd'])

    def get_info(self, status):
        def final():
            if accountName.get() == '' or csv_path.get() == '' \
                    or path.get() == '' or  ai_data_science_path.get() == '':
                messagebox.askokcancel("Alert", "It seems some fields are empty please fill it?")
                return
            else:
                if (self.info != {}) and (self.info['account_name'] != accountName.get().replace("'", "z").replace('"',
                                                                                                                   "z") or\
                        self.info['raw_csv_path'] != csv_path.get() or self.info['working_directory'] != path.get() or \
                        self.info['ai_datascience'] != ai_data_science_path.get() or self.info['work_type'] != r_v.get()\
                        or self.info['python_command_path'] != python_command_path.get()):
                    if status != -1:
                        if accountName.get().replace("'", "z").replace('"', "z") in [account for account in
                                                                                     status['all_accounts']]:
                            self.info = pickle.load(
                                open(os.path.join(os.path.join(os.getcwd(),
                                                               os.path.join('Dump',
                                                                            accountName.get().replace("'",
                                                                                                      "x").replace(
                                                                                '"', "x"))),
                                                  accountName.get().replace("'", "x").replace(
                                                      '"', "x") + '_info.pickle'),
                                     "rb"))
                        else: self.info = {}


                self.info['account_name'] = accountName.get().replace("'","x").replace('"', "x")
                self.info['raw_csv_path'] = csv_path.get()
                self.info['working_directory'] = path.get()
                self.info['ai_datascience'] = ai_data_science_path.get()
                self.info['work_type'] = r_v.get()
                self.info['python_command_path'] = python_command_path.get()
                self.update_info()
                self.initiate()
                self.fill_text()
                self.root.state('zoomed')
                self.root.deiconify()
                root.destroy()


        def close():
            root.withdraw()
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                root.destroy()
                self.root.destroy()
            else:
                root.deiconify()

        def clear_all_text():
            accountName.delete(0, "end")
            csv_path.delete(0, "end")
            path.delete(0, "end")
            ai_data_science_path.delete(0, "end")
            python_command_path.delete(0, "end")

        def update_ui():
            accountName.insert(0, self.info['account_name'])
            csv_path.insert(0, self.info["raw_csv_path"])
            path.insert(0, self.info['working_directory'])
            ai_data_science_path.insert(0, self.info['ai_datascience'])
            python_command_path.insert(0, self.info['python_command_path'])
            r_v.set(self.info['work_type'])

        def assign(selected):
            if selected == '\t-----\t':
                self.info = {}
                self.update_info()
                clear_all_text()
                return
            else:
                self.info = pickle.load(open(os.path.join(os.path.join(os.getcwd(),
                                                               os.path.join('Dump', selected)),
                                                          selected + '_info.pickle'),
                                     "rb"))
                clear_all_text()
                update_ui()



        self.root.withdraw()

        root = tk.Tk()
        # root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='HR_ICON.png'))
        root.wm_title("Generic Info")
        labelframe = tk.LabelFrame(root, text='Info')
        button_frame = tk.Frame(labelframe)
        radio_frame = tk.Frame(labelframe)

        # Label
        tk.Label(labelframe, text='Select Account : ').grid(column=0, padx=5, pady=5)
        tk.Label(labelframe, text='Account Name : ').grid(column=0, padx=5, pady=5)
        tk.Label(labelframe, text='Python command Path : ').grid(column=0, padx=5, pady=5)
        tk.Label(labelframe, text='CSV Path : ').grid(column=0, padx=5, pady=5)
        tk.Label(labelframe, text='Working Directory : ').grid(column=0, padx=5, pady=5)
        tk.Label(labelframe, text='Ai Datascience Path : ').grid(column=0, padx=5, pady=5)
        tk.Label(radio_frame, text='Work Type : ').grid(column=0, padx=5, pady=5)

        values = ['\t-----\t']
        if status != -1: values.extend(status['all_accounts'])
        variable = tk.StringVar(labelframe)

        if status != -1: variable.set(status['recent'].split("\\")[-1])
        else: variable.set('-')
        # Entry
        accountName = tk.Entry(labelframe, width=50)
        dropDownName = tk.OptionMenu(labelframe, variable, *values, command=assign)

        python_command_path = tk.Entry(labelframe, width=50)

        csv_path = tk.Entry(labelframe, width=50)
        button_csv_entry = tk.Button(labelframe, text='Choose', command=lambda: get_file(csv_path))

        path = tk.Entry(labelframe, width=50)
        button_file_entry = tk.Button(labelframe, text='Choose', command=lambda : get_dir(path))

        ai_data_science_path = tk.Entry(labelframe, width=50)
        button_ads_entry = tk.Button(labelframe, text='Choose', command=lambda: get_dir(ai_data_science_path))

        submit = tk.Button(button_frame, text='Submit', command=final)
        close_button = tk.Button(button_frame, text='Cancel', command=close)
        clear_button = tk.Button(button_frame, text='Clear', command=clear_all_text)


        values = {
            'Deduction Management System': 'DMS',
            'Collections': 'CLS'
        }

        r_v = tk.StringVar(root, "DMS")
        for i, (text, val) in enumerate(values.items()):
            tk.Radiobutton(radio_frame, text=text, variable=r_v, value=val).grid(row=0, column=i+1, padx=5, pady=5)

        dropDownName.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        accountName.grid(row=1, column=1, padx=5, pady=5)
        python_command_path.grid(row=2, column=1, padx=5, pady=5)

        csv_path.grid(row=3, column=1, padx=5, pady=5)
        button_csv_entry.grid(row=3, column=2, padx=5, pady=5)

        path.grid(row=4, column=1, padx=5, pady=5)
        button_file_entry.grid(row=4, column=2, padx=5, pady=5)

        ai_data_science_path.grid(row=5, column=1, padx=5, pady=5)
        button_ads_entry.grid(row=5, column=2, padx=5, pady=5)

        submit.grid(padx=10, pady=5, sticky='ew')
        close_button.grid(row=0, column=1, padx=10, pady=5)
        clear_button.grid(row=0, column=2, padx=10, pady=5)
        radio_frame.grid(row=6, columns=2, padx=2, pady=5, sticky='ew')
        button_frame.grid(row=7, column=1, pady=4, padx=2)

        root.protocol("WM_DELETE_WINDOW", close)
        labelframe.grid(padx=5, pady=5)

        if status != -1:
            clear_all_text()
            self.info = pickle.load(open(os.path.join(status['recent'],
                                                      status['recent'].split('\\')[-1] + '_info.pickle'), "rb"))
            update_ui()
            self.update_info()
        root.mainloop()

    def update_info(self):
        self.pre_processing_textbox.text_box_info = self.info
        self.aggregation_textbox.text_box_info = self.info
        self.model_trainer_textbox.text_box_info = self.info
        self.model_predictor_textbox.text_box_info = self.info

    def pre_load(self):
        dump_ = os.path.join(os.getcwd(), 'Dump')
        latest_file = {}
        if len(os.listdir(dump_)) == 0:
            return -1
        latest_file['recent'] = max([os.path.join(dump_, folder) for folder in os.listdir(dump_)], key=os.path.getmtime)
        latest_file['all_accounts'] = os.listdir(dump_)
        return latest_file


    def start_ui(self):
        status = self.pre_load()
        self.get_info(status)
        self.root.mainloop()
        # print(self.localhost.localPreProcessing.getPythonFunction())

    def make_batch(self):
        preprocessing_cmd = self.pre_processing_textbox.textbox.get("1.0", "end-1c")
        aggregation_cmd = self.aggregation_textbox.textbox.get("1.0", "end-1c")
        model_trainer_cmd = self.model_trainer_textbox.textbox.get("1.0", "end-1c")
        model_predictor_cmd = self.model_predictor_textbox.textbox.get("1.0","end-1c")

        if preprocessing_cmd == "" or \
            aggregation_cmd == "" or \
            model_trainer_cmd == "" or \
            model_predictor_cmd == "":
            messagebox.askokcancel("Alert", "Seems Some Fields in the textbox are empty.! please check.!")

        with open(os.path.join(os.path.join(self.info['master_path'], 'Commands'), "commands.txt"), "w") as file:
            file.write(preprocessing_cmd)
            file.write("\n\n")
            file.write(aggregation_cmd)
            file.write("\n\n")
            file.write(model_trainer_cmd)
            file.write("\n\n")
            file.write(model_predictor_cmd)
            file.write("\n\n")

        if ~preprocessing_cmd.startswith(r"C:\ProgramData\Anaconda3"):
            preprocessing_cmd = "C:/ProgramData/Anaconda3/"+preprocessing_cmd
            aggregation_cmd = "C:/ProgramData/Anaconda3/" + aggregation_cmd
            model_trainer_cmd = "C:/ProgramData/Anaconda3/" + model_trainer_cmd
            model_predictor_cmd = "C:/ProgramData/Anaconda3/" + model_predictor_cmd

        with open(os.path.join(os.path.join(self.info['master_path'], 'Commands'), "commands.bat"), "w") as file:
            file.write(preprocessing_cmd)
            file.write("\n\n")
            file.write(aggregation_cmd)
            file.write("\n\n")
            file.write(model_trainer_cmd)
            file.write("\n\n")
            file.write(model_predictor_cmd)
            file.write("\n\n")
            file.write("pause")
            file.write("\n")

    def analysis(self):
        def close():
            self.root.deiconify()
            root.destroy()

        def store_val():
            if predicted_key.get() == "" or actual_key.get() == "" or amount_key.get() == "":
                messagebox.askokcancel("Alert", "Some fields are empty Please check.!")
                return
            self.info['predicted_key'] = predicted_key.get()
            self.info['actual_key'] = actual_key.get()
            self.info['amount_key'] = amount_key.get()
            dump_data('predicted_key', predicted_key.get(), self.info)
            dump_data('actual_key', actual_key.get(), self.info)
            dump_data('amount_key', amount_key.get(), self.info)
            analyser_obj = analyser(root, self.info)


        self.root.withdraw()
        root = tk.Tk()
        pop_up_frame = tk.LabelFrame(root, text="Info")
        #
        tk.Label(pop_up_frame, text="Predicted Attribute Name :").grid(padx=5, pady=5)
        tk.Label(pop_up_frame, text="Actual Attribute Name :").grid(padx=5, pady=5)
        tk.Label(pop_up_frame, text="Amounnt Attribute Name :").grid(padx=5, pady=5)
        #
        predicted_key = tk.Entry(pop_up_frame, width=50)
        actual_key = tk.Entry(pop_up_frame, width=50)
        amount_key = tk.Entry(pop_up_frame, width=50)
        #
        if "predicted_key" in self.info.keys():
            set_val(predicted_key, self.info['predicted_key'])
            set_val(actual_key, self.info['actual_key'])
            set_val(amount_key, self.info['amount_key'])

        predicted_key.grid(row=0, column=1, padx=5, pady=5)
        actual_key.grid(row=1, column=1, padx=5, pady=5)
        amount_key.grid(row=2, column=1, padx=5, pady=5)
        #
        button_frame = tk.Frame(pop_up_frame)
        submit = tk.Button(button_frame, text="Submit", command=store_val)
        submit.grid(padx=8, pady=5)
        close = tk.Button(button_frame, text="Close", command=close)
        close.grid(row=0, column=1, padx=8, pady=5)
        button_frame.grid(padx=5, pady=5, row=3, column=1)

        pop_up_frame.grid(padx=5, pady=5)
        root.protocol("WM_DELETE_WINDOW", close)
        root.mainloop()

    def add_scoring(self):
        def close():
            self.root.deiconify()
            self.root.state("zoomed")
            self.temp_root.destroy()

        def running():
            if self.new_text_box.t1 == None:
                self.temp_root.after(self.normal_hitrate, running)
                return
            elif self.new_text_box.t1.isAlive():
                self.temp_root.after(self.execution_hitrate, running)
                return
            else:
                self.new_text_box.show_message()
                self.new_text_box.execute_button['state'] = 'active'
                self.temp_root.after(self.normal_hitrate, running)
                self.new_text_box.t1 = None

        self.root.withdraw()
        self.temp_root = tk.Tk()
        self.new_text_box = scoring(self.temp_root, width=80, height=20, label="scoring")
        self.new_text_box.text_box_info = pickle.load(open(os.path.join(self.info["dump_path"],
                                                              self.info["account_name"] + "_info.pickle"), "rb"))
        self.new_text_box.popup_button.grid_forget()
        self.temp_root.after(self.normal_hitrate, running)
        self.temp_root.resizable(0, 0)
        self.temp_root.protocol("WM_DELETE_WINDOW", close)
        self.temp_root.mainloop()

    def execute_all(self):
        executions = [self.pre_processing_textbox, self.aggregation_textbox,
                      self.model_trainer_textbox, self.model_predictor_textbox]
        for executable in executions:
            # if executable.get_text() == "":
            #     messagebox.askokcancel("Alert", f"Seems {executable.label} textbox is Empty!")
            #     return
            executable.execute()
            while executable.t1.isalive():
                pass

    def execute(self):
        thread = threading.Thread(target=self.execute_all)
        thread.daemon = True
        thread.start()

    def make_file_menu(self):
        menu = tk.Menu(self.root)

        file = tk.Menu(menu)
        file.add_command(label='Change Account', command=self.start_ui)
        # file.add_command(label='Execute All', command=self.execute)
        file.add_command(label='Add Scoring', command=self.add_scoring)
        file.add_command(label='Generate Commands', command=self.make_batch)
        file.add_command(label='Generate Analysis', command=self.analysis)
        file.add_command(label='Close', command=quit)

        menu.add_cascade(label='File', menu=file)
        tk.Tk.config(self.root, menu=menu)
        return menu

    def ret_(self):
        pass


if __name__ == '__main__':
    ctrl = controllerUI()
    ctrl.run()
