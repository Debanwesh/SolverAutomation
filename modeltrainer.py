from TextBox import textBox
import tkinter as tk
import os
from utility import *

class modeltrainer(textBox):

    def __init__(self, master, row=0, col=0, label='My Label', width=70, height=15):
        super().__init__(master, row, col, label, width, height)
        # self.p1 = None
        # self.destry_process()

    def make_command(self):
        if 'aggregate_file_paths' not in self.text_box_info.keys():
            val = get_data("aggregate_file_paths", self.text_box_info)
            if val is not None: self.text_box_info['aggregate_file_paths'] = val
            else:
                messagebox.askokcancel("Alert", "Didn't find any aggregation path keys please configure "
                                            "aggregation module or find me :)")
                return
        cmd = self.get_top_line()
        model_dir = os.path.join(self.text_box_info['master_path'], 'Model')
        preprocessed_file_path = os.path.join(os.path.join(self.text_box_info['master_path'],
                                                                                 'PreProcessed'), 'preprocessed.csv')
        cmd += "'preprocessed_file_path':'"+preprocessed_file_path+"',"
        cmd += "'aggregate_file_paths':'" + self.text_box_info['aggregate_file_paths'] + "',"
        _key_ = self.label+"_object_list"
        _dict_ = self.text_box_info[_key_]
        _id_ = 1
        model_paths = ''
        cmd += "'"+_key_+"':["
        for key, val in _dict_.items():
            model_paths += os.path.join(model_dir,key.replace(",","_")+".pkl") + ","
            cmd += "{'target_model_file_path':'" + os.path.join(model_dir,key.replace(",","_")+".pkl") + "',"
            cmd += "'python_function':'" + val['function'] + "',"
            cmd += "'model_shortname':'" + key + "',"
            cmd += "'arguments':'" + val['arguments'] +"',"
            cmd += "'model_id':'"+str(_id_)+"'},"
            _id_ += 1
        cmd += "],}"
        cmd = cmd.replace("\\", "/")
        model_paths = model_paths.replace("\\", "/")
        dump_data('model_cmd', cmd, self.text_box_info)
        dump_data('model_paths', model_paths, self.text_box_info)

        self.clear_textbox()
        self.textbox.insert(tk.INSERT, cmd)
        self.formatted = False

    # def entry(self):
    #
    #     exist = False
    #     model_trainer_info = {}
    #     if 'model_generators_object_list' in self.text_box_info.keys():
    #         exist=True
    #         model_trainer_info = self.text_box_info['model_generators_object_list']
    #
    #
    #     def close():
    #         self.entry_button['state'] = 'active'
    #         master_root.destroy()
    #
    #     def entry_model(b1, b2, frame):
    #         revisit=False
    #         if b1.cget("text") in model_trainer_info.keys(): revisit=True
    #         def close_root():
    #             master_root.deiconify()
    #             root.destroy()
    #
    #         def submit():
    #             if model_shortname.get() == "" or python_function.get() == "" or arguments.get() == "":
    #                 messagebox.askokcancel("Alert", "Hmmm..., Seems you left a field empty :(, plz check.!")
    #                 return
    #
    #             if revisit: del model_trainer_info[b1.cget('text')]
    #
    #             model_trainer_info[model_shortname.get()] = {}
    #             model_trainer_info[model_shortname.get()]['python_function'] = python_function.get()
    #             model_trainer_info[model_shortname.get()]['arguments'] = arguments.get()
    #             b1.config(text=model_shortname.get(), command=lambda: entry_model(b1, b2, frame))
    #             b2.config(state="active")
    #             if not revisit or b1.cget("text") == "Add":
    #                 row=make_model_entry()
    #                 submit_model.grid(row=row+1)
    #             master_root.deiconify()
    #             root.destroy()
    #
    #         master_root.withdraw()
    #         root = tk.Tk()
    #         pop_frame = tk.LabelFrame(root, text="Details")
    #         #Label
    #         tk.Label(pop_frame, text="Model Name : ").grid(padx=5, pady=5)
    #         tk.Label(pop_frame, text="Python Function : ").grid(padx=5, pady=5)
    #         tk.Label(pop_frame, text="Arguments : ").grid(padx=5, pady=5)
    #         #Entry
    #         model_shortname = tk.Entry(pop_frame, width=50)
    #         python_function = tk.Entry(pop_frame, width=50)
    #         arguments = tk.Entry(pop_frame, width=50)
    #         if revisit:
    #             set_val(model_shortname, b1.cget("text"))
    #             set_val(python_function, model_trainer_info[b1.cget("text")]["python_function"])
    #             set_val(arguments, model_trainer_info[b1.cget("text")]["arguments"])
    #         # Grid
    #         model_shortname.grid(row=0, column=1, padx=5, pady=5)
    #         python_function.grid(row=1, column=1, padx=5, pady=5)
    #         arguments.grid(row=2, column=1, padx=5, pady=5)
    #         # Button
    #         submit = tk.Button(pop_frame, text="Submit", command=submit)
    #         submit.grid(column=1, padx=5, pady=5)
    #         pop_frame.grid(padx=5, pady=5)
    #
    #         root.protocol("WM_DELETE_WINDOW", close_root)
    #         root.mainloop()
    #
    #     def remove_button(button, frame):
    #         del model_trainer_info[button.cget("text")]
    #         remove_frame(frame)
    #
    #     def remove_frame(frame, key=None):
    #         if key != None: del model_trainer_info[key]
    #         frame.grid_forget()
    #         frame.destroy()
    #
    #     def make_model_entry(key=None):
    #         entry_frame = tk.Frame(pop_up_frame)
    #         button_add = tk.Button(entry_frame, text="Add")
    #         button_remove = tk.Button(entry_frame, text="Remove", state="disabled")
    #         if key==None:
    #             button_add.config(command=lambda: entry_model(button_add, button_remove, entry_frame))
    #             button_remove.config(command=lambda: remove_button(button_add, entry_frame))
    #         else:
    #             button_add.config(command=lambda: entry_model(button_add, button_remove, entry_frame),
    #                               text=key)
    #             button_remove.config(command=lambda: remove_button(button_add, entry_frame),state='active')
    #
    #         button_add.grid(padx=5, pady=5)
    #         button_remove.grid(row=0, column=1, padx=5, pady=5)
    #         entry_frame.grid(padx=5, pady=5)
    #         return entry_frame.grid_info().get("row")
    #
    #     def done_model_trainer():
    #         self.text_box_info['model_generators_object_list'] = model_trainer_info
    #         self.dump_data("model_generators_object_list", model_trainer_info)
    #         self.make_train_query()
    #         close()
    #
    #
    #     self.entry_button['state'] = 'disabled'
    #     master_root = tk.Tk()
    #     pop_up_frame = tk.LabelFrame(master_root, text=self.label)
    #     submit_model = tk.Button(pop_up_frame, text="Submit", command=done_model_trainer)
    #     if not exist: make_model_entry()
    #     else:
    #         for key in model_trainer_info.keys():
    #             make_model_entry(key)
    #         make_model_entry()
    #
    #     submit_model.grid(padx=5, pady=5)
    #     pop_up_frame.grid(padx=5, pady=5)
    #
    #     master_root.protocol("WM_DELETE_WINDOW", close)
    #     master_root.mainloop()

    # def make_model_list(self):
    #     _id = 1
    #     self.text_box_info['model_paths'] = "'"
    #     q = "'model_generators_object_list':["
    #     for key, val in self.text_box_info['model_generators_object_list'].items():
    #         self.text_box_info['model_paths'] += os.path.join(os.path.join(self.text_box_info['master_path'],
    #                                                                       'Model'),key+".pkl',") + ","
    #         q += "{'target_model_file_path':'"+ os.path.join(os.path.join(self.text_box_info['master_path'],
    #                                                                       'Model'),key+".pkl',")
    #         q += "'python_function':'"+val['python_function']+"',"
    #         q += "'model_shortname':'"+key+"',"
    #         q += "'arguments':'"+val['arguments']+"',"
    #         q += "'model_id':'"+str(_id)+"'},"
    #         _id += 1
    #     self.text_box_info['model_paths'] += "'"
    #     q += "]"
    #     return q



    # def make_train_query(self):
    #     query = self.get_top_line()
    #     if "preprocessed_file_path" in self.text_box_info.keys():
    #         preprocess_file_path = self.text_box_info["preprocessed_file_path"]
    #     else:
    #         preprocess_file_path = os.path.join(os.path.join(self.text_box_info['master_path'],
    #                                                                         'PreProcessed'), 'preprocessed.csv')
    #
    #     preprocess_file_path = "{'preprocessed_file_path':'"+preprocess_file_path+"',"
    #     if 'aggregate_file_paths' not in self.text_box_info.keys():
    #         messagebox.askokcancel("Alert",
    #                                "Hmmmm.... seems you missed Seq file data make sure you configured aggregation")
    #         raise Exception("Seq CSV not found configure Aggregation section for same")
    #     aggregate_file_paths = "'aggregate_file_paths':'"+self.text_box_info['aggregate_file_paths'] + "',"
    #     model_generators_object_list = self.make_model_list()+"}"
    #     cmd = query + preprocess_file_path + aggregate_file_paths + model_generators_object_list
    #     cmd = cmd.replace("\\", "/")
    #     self.clear_textbox()
    #     self.textbox.insert(tk.INSERT, cmd)
    #     self.text_box_info['model_trainer_cmd'] = cmd
    #     self.dump_data("model_trainer_cmd", cmd)
    #     self.dump_data("model_paths", self.text_box_info['model_paths'])
    #     self.formatted=False

    # def destry_process(self):
    #     if self.p1 == None:
    #         self.master.after(3000, self.destry_process)
    #         return
    #     elif self.p1.is_alive():
    #         self.master.after(3000, self.destry_process)
    #         return
    #     else:
    #         self.p1 = None
    #         self.execute_button['state'] = 'active'

    #
    # def execute(self):
    #     self.execute_button['state'] = 'disabled'
    #     if self.formatted:
    #         self.formatUI()
    #     self.execute_command = self.get_text()
    #
    #     if len(self.execute_command.split(' ')) != 4 or self.formatted:
    #         self.execute_button['state'] = 'active'
    #         raise Exception("Something is Fishy in your query, GEE, find me :_)")
    #     try:
    #
    #         if 'train_work' not in self.text_box_info.keys():
    #
    #             key_highlight = 'target_model_file_path'
    #             indices = ()
    #             for match in re.finditer(key_highlight, self.execute_command):
    #                 indices += (match.start(),)
    #             indices = tuple(map(lambda x: x - 2, indices))
    #             indices += (-2,)
    #             work = []
    #             for inds, inde in zip(indices[:-1:], indices[1::]):
    #                 query = self.execute_command[:indices[0]]
    #                 query += self.execute_command[inds:inde] + "]}"
    #                 work.append(query)
    #             self.text_box_info['train_work'] = work
    #
    #         self.pool = ()
    #         for w in self.text_box_info['train_work']:
    #             p = multiprocessing.Process(target=os.system, args=(w,))
    #             self.pool += (p,)
    #         [p.start() for p in self.pool]
    #     except Exception as e:
    #         print(e)
    #         self.execute_button['state'] = 'active'

