import tkinter as tk
from TextBox import textBox
import os
from utility import *

class preprocessing(textBox):

    def __init__(self, master, row=0, col=0, label='My Label', width=70, height=15):
        super().__init__(master, row, col, label, width, height)
        # self.destry_process()

    def make_command(self):
        cmd = self.get_top_line()
        preprocessed_file_path = os.path.join(os.path.join(self.text_box_info['master_path'],
                                                                                 'PreProcessed'), 'preprocessed.csv')
        cmd += "'raw_file_paths':'"+self.text_box_info['raw_csv_path'] +"',"
        cmd += "'preprocessed_file_path':'"+preprocessed_file_path+"',"

        _key_ = self.label+"_object_list"
        _dict_ = self.text_box_info[_key_]
        _id_ = 1
        cmd += "'"+_key_+"':["
        for key, val in _dict_.items():
            cmd += "{'python_function':'" + val['function'] + "',"
            cmd += "'preprocess_shortname':'" + key + "',"
            cmd += "'arguments':'" + val['arguments'] +"',"
            cmd += "'preprocess_id':'"+str(_id_)+"'},"
            _id_ += 1
        cmd += "],}"
        cmd = cmd.replace("\\", "/")
        dump_data('preprocessed_file_path', preprocessed_file_path, self.text_box_info)
        dump_data('preprocess_cmd', cmd, self.text_box_info)

        self.clear_textbox()
        self.textbox.insert(tk.INSERT, cmd)




    # def destry_process(self):
    #     if self.p1 == None:
    #         self.master.after(3000, self.destry_process)
    #         return
    #     elif self.p1.is_alive():
    #         self.master.after(3000, self.destry_process)
    #         return
    #     else:
    #         self.p1 = None
    #
    #         self.execute_button['state'] = 'active'
    #
    # def execute(self):
    #     self.execute_button['state'] = 'disabled'
    #     if self.formatted:
    #         self.formatUI()
    #     self.execute_command = self.get_text()
    #     if len(self.execute_command.split(' ')) != 4 or self.formatted:
    #         self.execute_button['state'] = 'active'
    #         raise Exception("Something is Fishy in your query, GEE, find me :_)")
    #     try:
    #         self.p1 = multiprocessing.Process(target=os.system, args=(self.execute_command,))
    #         self.p1.start()
    #     except Exception as e:
    #         print(e)
    #         self.execute_button['state'] = 'active'
    #
    # def make_preprocess_query(self):
    #     self.text_box_info['preprocessed_file_path'] = os.path.join(os.path.join(self.text_box_info['master_path'],
    #                                                                              'PreProcessed'), 'preprocessed.csv')
    #     self.dump_data("preprocessed_file_path", self.text_box_info['preprocessed_file_path'])
    #     query = self.get_top_line()
    #     list_arg = "{" + self.make_list_query('preprocessing_object_list', self.text_box_info)
    #     list_arg += "'raw_file_paths':'"+self.text_box_info['raw_csv_path']+"','preprocessed_file_path':'"\
    #                 +self.text_box_info['preprocessed_file_path']+"'}"
    #     cmd = query.replace("\\", "/") + list_arg
    #     self.clear_textbox()
    #     self.textbox.insert(tk.INSERT, cmd)
    #     self.text_box_info['preprocess_cmd'] = cmd
    #     self.dump_data('preprocess_cmd', cmd)
    #     self.formatted = False

    # def entry(self):
    #     self.entry_button['state'] = 'disabled'
    #
    #     def update_info():
    #         if python_function_entry.get() != '' and preprocess_shortname_entry.get() != '' and arguments_entry.get() \
    #                 != '' and preprocess_id__entry.get() != '':
    #             info = {}
    #             info['python_function'] = python_function_entry.get()
    #             info['preprocess_shortname'] = preprocess_shortname_entry.get()
    #             info['arguments'] = arguments_entry.get()
    #             info['preprocess_id'] = preprocess_id__entry.get()
    #             self.text_box_info['preprocessing_object_list'] = info
    #             self.make_preprocess_query()
    #             self.dump_data('preprocessing_object_list', info)
    #             self.entry_button['state'] = 'active'
    #             root.destroy()
    #         else:
    #             if messagebox.askokcancel("Quit", "It seems some fields are empty wanna quit?"):
    #                 root.destroy()
    #
    #
    #     root = tk.Tk()
    #     popupframe = tk.LabelFrame(root, text=self.label)
    #     # Labels
    #     tk.Label(popupframe, text='Python Function : ').grid(column=0, padx=5, pady=5)
    #     tk.Label(popupframe, text='Preprocess Shortname : ').grid(column=0, padx=5, pady=5)
    #     tk.Label(popupframe, text='Arguments : ').grid(column=0, padx=5, pady=5)
    #     tk.Label(popupframe, text='Pre Process ID : ').grid(column=0, padx=5, pady=5)
    #     #Entry
    #     python_function_entry = tk.Entry(popupframe, width=50)
    #     preprocess_shortname_entry = tk.Entry(popupframe, width=50)
    #     arguments_entry = tk.Entry(popupframe, width=50)
    #     preprocess_id__entry = tk.Entry(popupframe, width=50)
    #     #
    #     if 'preprocessing_object_list' in self.text_box_info.keys():
    #         set_val(python_function_entry, self.text_box_info['preprocessing_object_list']['python_function'])
    #         set_val(preprocess_shortname_entry, self.text_box_info['preprocessing_object_list']['preprocess_shortname'])
    #         set_val(arguments_entry, self.text_box_info['preprocessing_object_list']['arguments'])
    #         set_val(preprocess_id__entry, self.text_box_info['preprocessing_object_list']['preprocess_id'])
    #
    #
    #     # Button
    #     buttonFrame = tk.Frame(popupframe)
    #     submit = tk.Button(buttonFrame, text='Submit', command=update_info)
    #     python_function_entry.grid(row=0, column=1, padx=5, pady=5)
    #     preprocess_shortname_entry.grid(row=1, column=1, padx=5, pady=5)
    #     arguments_entry.grid(row=2, column=1, padx=5, pady=5)
    #     preprocess_id__entry.grid(row=3, column=1, padx=5, pady=5)
    #
    #     submit.grid(padx=5, pady=5)
    #     buttonFrame.grid(column=1, padx=5, pady=5)
    #     popupframe.grid(padx=5, pady=5)
    #     root.mainloop()
