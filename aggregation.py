import tkinter as tk
from TextBox import textBox
from collections import OrderedDict
from utility import *
import os, re


class aggregation(textBox):

    def __init__(self, master, row=0, col=0, label='My Label', width=70, height=15):
        super().__init__(master, row, col, label, width, height)
        self.aggregation_object_id = 0
        # self.destry_process()

    def entry(self):
        is_empty = True
        if "aggregation_object_list" in self.text_box_info.keys(): is_empty = False
        if not is_empty: aggregation_info = self.text_box_info["aggregation_object_list"]
        else: aggregation_info = OrderedDict()

        def entry_aggregation_column(agg_obj, agg_but1, agg_but2, agg_frame):
            if agg_obj == '':
                messagebox.askokcancel('alert', "Aggregation Object Can't Be empty")
                return

            revisit=False
            if agg_obj in aggregation_info.keys(): revisit=True
            if not revisit: aggregation_info[agg_obj] = OrderedDict()

            def get_button(values=None):
                frame = tk.Frame(pop_frame)
                if values != None:
                    b1 = tk.Button(frame, text=values['output_key'])
                    b2 = tk.Button(frame, text="Remove")
                else:
                    b1 = tk.Button(frame, text="Add")
                    b2 = tk.Button(frame, text="Remove", state="disabled")

                if values != None: b1.config(command=lambda: pop_up_form(b1, b2, values))
                else: b1.config(command=lambda: pop_up_form(b1, b2))

                b2.config(command=lambda: remove_button(b1, frame))
                b1.grid(padx=5, pady=5, sticky="ew")
                b2.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
                frame.grid(padx=5, pady=5, sticky="we")
                row = frame.grid_info().get("row")
                button.grid(row=row + 1, padx=5, pady=5)

            def remove_button(button, frame):
                del aggregation_info[agg_obj][button.cget("text")]
                remove_frame(frame)

            def pop_up_form(button1, button2, values=None):

                def fill():
                    if output_key.get() == '' or python_function.get() == '' or arguments.get() == '':
                        messagebox.askokcancel('alert', "Fields can't be empty :)")
                        return

                    info = dict()
                    info['output_key'] = output_key.get()
                    info['python_function'] = python_function.get()
                    info['arguments'] = arguments.get()
                    aggregation_info[agg_obj][output_key.get()] = info
                    if not revisit:
                        get_button()
                    else:
                        if button1.cget("text") == "Add": get_button()
                    button1.config(text=output_key.get())
                    button2.config(state='active')
                    root.deiconify()
                    master.destroy()

                def close_root():
                    root.deiconify()
                    master.destroy()

                root.withdraw()
                master = tk.Tk()
                lbl_frm = tk.LabelFrame(master, text="Aggregation Columns")
                # Label
                tk.Label(lbl_frm, text="Output Key : ").grid(padx=3, pady=3)
                tk.Label(lbl_frm, text="python Function : ").grid(padx=3, pady=3)
                tk.Label(lbl_frm, text="Arguments : ").grid(padx=3, pady=3)
                # Entry
                output_key = tk.Entry(lbl_frm, width=50)
                output_key.focus_set()
                python_function = tk.Entry(lbl_frm, width=50)
                arguments = tk.Entry(lbl_frm, width=50)
                if values != None:
                    set_val(output_key, values['output_key'])
                    set_val(python_function, values['python_function'])
                    set_val(arguments, values['arguments'])
                ## Grid
                output_key.grid(row=0, column=1, padx=3, pady=3)
                python_function.grid(row=1, column=1, padx=3, pady=3)
                arguments.grid(row=2, column=1, padx=3, pady=3)
                # Button
                submit = tk.Button(lbl_frm, text="Submit", command=fill)
                submit.grid(column=1, padx=5, pady=5)

                lbl_frm.grid(padx=3, pady=3, sticky="ew")
                master.protocol("WM_DELETE_WINDOW", close_root)
                master.mainloop()

            def agg_cols_done():
                agg_but1.config(text="Aggregated", command=lambda: entry_aggregation_column(agg_obj, agg_but1,
                                                                                            agg_but2, agg_frame))
                agg_but2.config(text="Remove", command=lambda : remove_frame(agg_frame, agg_obj), state="active")
                if not revisit:
                    row = make_aggregation_entry()
                    submit.grid(row=row+1)
                master_root.deiconify()
                root.destroy()

            def close_master():
                master_root.deiconify()
                root.destroy()

            master_root.withdraw()
            root = tk.Tk()
            pop_frame = tk.LabelFrame(root, text="Aggregation Column")
            button = tk.Button(pop_frame, text="Done", command=agg_cols_done)
            button.grid(padx=5, pady=5, sticky="ew")

            if not revisit: get_button()
            else:
                for key in aggregation_info[agg_obj].keys():
                    get_button(aggregation_info[agg_obj][key])
                get_button()


            pop_frame.grid(padx=3, pady=3)
            root.protocol("WM_DELETE_WINDOW", close_master)
            root.mainloop()

        def remove_frame(frame, key=None):
            if key != None: del aggregation_info[key]
            frame.grid_forget()
            frame.destroy()

        def make_aggregation_entry(key=None):

            frame = tk.Frame(pop_up_frame)
            tk.Label(frame, text="Aggregation Object : ").grid(padx=5, pady=5)
            if key == None:
                entry = tk.Entry(frame, width=50)
                button1 = tk.Button(frame, text="Aggregation Object",
                                    command=lambda: entry_aggregation_column(entry.get(), button1, button2, frame))
                button2 = tk.Button(frame, text="Remove", state="disabled")
            else:
                entry = tk.Entry(frame, width=50)
                set_val(entry, key)
                button1 = tk.Button(frame, text="Aggregated",
                                    command=lambda: entry_aggregation_column(entry.get(), button1, button2, frame))
                button2 = tk.Button(frame, text="Remove", command=lambda : remove_frame(frame, entry.get()))
            entry.focus_set()
            entry.grid(row=0, column=1, padx=5, pady=5)
            button1.grid(row=0, column=2, padx=5, pady=5)
            button2.grid(row=0, column=3, padx=5, pady=5)
            frame.grid(padx=5, pady=5)
            self.aggregation_object_id += 1
            return frame.grid_info().get("row")

        def done_agg():
            self.text_box_info["aggregation_object_list"] = aggregation_info
            dump_data('aggregation_object_list', aggregation_info, self.text_box_info)
            self.make_agg_query()
            close()

        def close():
            self.entry_button['state'] = 'active'
            master_root.destroy()


        self.entry_button['state'] = 'disabled'
        master_root = tk.Tk()
        pop_up_frame = tk.LabelFrame(master_root, text=self.label)
        submit = tk.Button(pop_up_frame, text="Submit", command = done_agg)
        if is_empty: make_aggregation_entry()
        else:
            for key in aggregation_info.keys():
                make_aggregation_entry(key)
            make_aggregation_entry()

        submit.grid(padx=5, pady=5, )
        pop_up_frame.grid(padx=5, pady=5)
        master_root.protocol("WM_DELETE_WINDOW", close)
        master_root.mainloop()

    def make_agg_columns_query(self, val):
        query = "'aggregation_columns':["
        for _dict_ in val:
            query = query + "{"
            for key, value in _dict_.items():
                query = query + "'" + key + "':'" + value + "',"
            query = query + "},"
        query = query + "]"
        return query


    def make_agg_query(self):
        agg_path = os.path.join(self.text_box_info['master_path'], 'Aggregation')

        preprocessed_file_path = os.path.join(os.path.join(self.text_box_info['master_path'],
                                                                                 'PreProcessed'), 'preprocessed.csv')
        aggregate_file_paths = ''
        _id = 1
        query = self.get_top_line()
        query = query + "'preprocessed_file_path':'" + preprocessed_file_path + "',"
        aggregation_object_list = "'aggregation_object_list':["
        for key, val in self.text_box_info['aggregation_object_list'].items():
            aggregation_object_list += "{"
            aggregation_object_list = aggregation_object_list + "'aggregation_object_id':" + str(_id) + ","
            aggregation_object_list = aggregation_object_list + "'aggregation_object':'" + key + "',"
            aggregation_object_list = aggregation_object_list + "'aggregation_target_file_path':'" +\
                                      os.path.join(agg_path, key.replace(",", "_") + ".csv") + "',"
            aggregate_file_paths += os.path.join(agg_path, key.replace(",", "_") + ".csv") + ","
            aggregation_object_list = aggregation_object_list + self.make_agg_columns_query(
                self.text_box_info['aggregation_object_list'][key].values())
            aggregation_object_list += "},"
            _id += 1
        aggregation_object_list += "]}"
        cmd = query + aggregation_object_list
        cmd = cmd.replace("\\", "/")
        self.clear_textbox()
        print(cmd)
        self.textbox.insert(tk.INSERT, cmd)
        self.text_box_info['aggregation_cmd'] = cmd
        self.text_box_info['aggregate_file_paths'] = aggregate_file_paths.strip(",")
        dump_data("aggregation_cmd", cmd, self.text_box_info)
        dump_data("aggregate_file_paths", aggregate_file_paths.strip(","), self.text_box_info)
        self.formatted = False

    def make_work(self):
        work = ()
        start, end = self.execute_command.find("["), self.execute_command.rfind("]")
        for string in re.findall(r"{(.*?(\[.*?\]).*?)}", self.execute_command[start:end]):
            work += (self.execute_command[:start+1] + "{" + string[0] + "}" + self.execute_command[end:], )
        return work

    # def execute(self):
    #     # self.execute_button['state'] = 'disabled'
    #     if self.formatted:
    #         self.formatUI()
    #     self.execute_command = self.get_text()
    #
    #     if len(self.execute_command.split(' ')) != 4 or self.formatted:
    #         self.execute_button['state'] = 'active'
    #         raise Exception("Something is Fishy in your query, GEE, find me :_)")
    #
    #     # self.pool = multiprocessing.Pool(multiprocessing.cpu_count())
    #     # self.pool.map(os.system, work)
    #
    #     work = self.make_work()
    #     print(work)
    #
    #     self.pool = ()
    #     for w in work:
    #         p = multiprocessing.Process(target=os.system, args=(w, ))
    #         p.start()
    #         self.pool += (p, )
    # #
    # # def destry_process(self):
    # #     if self.pool == None:
    # #         self.master.after(3000, self.destry_process)
    #         return
    #     elif any(p.is_alive() for p in self.pool):
    #         self.master.after(3000, self.destry_process)
    #         return
    #     else:
    #         self.pool = None
    #         self.execute_button['state'] = 'active'


