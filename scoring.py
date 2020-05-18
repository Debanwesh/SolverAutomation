import tkinter as tk
from TextBox import textBox
import os
from utility import *

class scoring(textBox):

    def __init__(self, master, row=0, col=0, label='My Label', width=70, height=15):
        super().__init__(master, row, col, label, width, height)


    def entry(self):

        exist=False
        if self.label + "_object_list" in self.text_box_info.keys():  exist=True
        if exist: info = self.text_box_info[self.label + "_object_list"]
        else: info={}


        def form(add, remove, frame):

            revisit=False
            if add.cget("text") in info.keys(): revisit=True

            def close_form():
                master_root.deiconify()
                root.destroy()

            def fill_entry():
                if entry_arguments.get() == '' or entry_python_function.get() == '' or entry_shortname.get() == '' or \
                        entry_actual.get() == '' or entry_predicted.get() == '':
                    messagebox.askokcancel("Alert", "Umm.. Some fields are empty please check")
                    return

                if revisit and entry_shortname.get() != add.cget('text'):
                    self.remove_key(info, add.cget('text'))

                info[entry_shortname.get()] = {}
                info[entry_shortname.get()]['function'] = entry_python_function.get().replace("#", ".")
                info[entry_shortname.get()]['arguments'] = entry_arguments.get()
                info[entry_shortname.get()]['actual'] = entry_actual.get()
                info[entry_shortname.get()]['predicted'] = entry_predicted.get()
                add.config(text=entry_shortname.get())
                remove.config(state='active', command=lambda: self.remove_frame(add, info, frame))
                if not revisit or add.cget("text") == "Add":
                    row=add_button()
                    submit_button.grid(row=row+1)
                close_form()

            master_root.withdraw()
            root = tk.Tk()
            root.wm_title("Details")
            lbl_frm = tk.LabelFrame(root, text="Details")
            # root.lift()
            # root.attributes("-topmost", True)
            #
            tk.Label(lbl_frm, text="Name : ").grid(row=0, column=0, padx=5, pady=5)
            tk.Label(lbl_frm, text="Python Function : ").grid(row=1, column=0, padx=5, pady=5)
            tk.Label(lbl_frm, text="Arguments : ").grid(row=2, column=0, padx=5, pady=5)
            tk.Label(lbl_frm, text="Actual : ").grid(row=3, column=0, padx=5, pady=5)
            tk.Label(lbl_frm, text="Predicted : ").grid(row=4, column=0, padx=5, pady=5)
            #
            entry_shortname = tk.Entry(lbl_frm, width=50)
            entry_shortname.focus_set()
            entry_python_function = tk.Entry(lbl_frm, width=50)
            entry_arguments = tk.Entry(lbl_frm, width=50)
            entry_actual = tk.Entry(lbl_frm, width=50)
            entry_predicted = tk.Entry(lbl_frm, width=50)
            #
            if revisit:
                set_val(entry_shortname, add.cget("text"))
                set_val(entry_python_function, info[add.cget("text")]['function'])
                set_val(entry_arguments, info[add.cget("text")]['arguments'])
                set_val(entry_actual, info[add.cget("text")]['actual'])
                set_val(entry_predicted, info[add.cget("text")]['predicted'])
            #
            entry_shortname.grid(row=0, column=1, padx=5, pady=5)
            entry_python_function.grid(row=1, column=1, padx=5, pady=5)
            entry_arguments.grid(row=2, column=1, padx=5, pady=5)
            entry_actual.grid(row=3, column=1, padx=5, pady=5)
            entry_predicted.grid(row=4, column=1, padx=5, pady=5)
            #
            done = tk.Button(lbl_frm, text="Done", command=fill_entry)
            done.grid(column=1, padx=5, pady=5)

            lbl_frm.grid(padx=5, pady=5, sticky="we")
            root.protocol("WM_DELETE_WINDOW", close_form)
            root.resizable(0, 0)
            root.mainloop()


        def add_button(key=None):
            frame = tk.Frame(pop_up_frame)

            if key == None:
                add = tk.Button(frame, text="Add")
                remove = tk.Button(frame, text="Remove", state="disabled")
            else:
                add = tk.Button(frame, text=key)
                remove = tk.Button(frame, text="Remove", state="active",
                                   command=lambda: self.remove_frame(add, info, frame))

            add.config(command=lambda: form(add, remove, frame))

            add.grid(padx=8, pady=5)
            remove.grid(row=0, column=1,padx=8, pady=5)
            frame.grid(padx=8, pady=5)
            return frame.grid_info().get("row")

        def close():
            self.retrive_entry(info)
            master_root.destroy()


        master_root = tk.Tk()
        # master_root.lift()
        master_root.wm_title("Object List Info")
        pop_up_frame = tk.LabelFrame(master_root, text=self.label)
        if not exist: add_button()
        else:
            for key in info.keys():
                add_button(key)
            add_button()
        submit_button = tk.Button(pop_up_frame, text="Submit", command=close)
        submit_button.grid(padx=5, pady=5)
        pop_up_frame.grid(padx=5, pady=5, sticky="ew")
        master_root.resizable(0, 0)
        master_root.mainloop()



    def make_command(self):

        cmd = self.get_top_line()
        test_file_path = self.text_box_info['pred_path']
        model_score_filepath = os.path.join(os.path.join(self.text_box_info['master_path'], "Analysed"),
                                            "scoring.csv")

        _key_ = self.label+"_object_list"
        _dict_ = self.text_box_info[_key_]
        _id_ = 1
        cmd += "'"+self.label+"_object"+"':["
        for key, val in _dict_.items():
            cmd += "{'scoring_id':'"+str(_id_)+"',"
            cmd += "'scoring_shortname':'" + key + "',"
            cmd += "'test_file_path':'" + test_file_path + "',"
            cmd += "'python_function':'" + val['function'] + "',"
            cmd += "'actual_header':'" + val['actual'] + "',"
            cmd += "'predicted_header':'" + val['predicted'] + "',"
            cmd += "'arguments':'" + val['arguments'] +"',"
            cmd += "'model_score_filepath':'"+model_score_filepath+"'},"
            _id_ += 1
        cmd += "],}"
        cmd = cmd.replace("\\", "/")
        dump_data('model_score_filepath', model_score_filepath, self.text_box_info)
        dump_data('scoring_cmd', cmd, self.text_box_info)
        self.clear_textbox()
        self.textbox.insert(tk.INSERT, cmd)