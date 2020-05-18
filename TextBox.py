import tkinter as tk
import json
import pickle
import os, re, subprocess
from utility import *
import pyperclip
import queue
import multiprocessing, threading


class textBox:

    def __init__(self, master, row=0, col=0, label='My Label', width=70, height=15):
        self.master = master
        self.text_box_info = {}

        self.labelframe = tk.LabelFrame(master, text=label)
        self.scroll = tk.Scrollbar(self.labelframe)
        self.textbox = tk.Text(self.labelframe, width=width, height=height, yscrollcommand= self.scroll.set)
        self.button_frame = tk.Frame(self.labelframe)
        self.label = label

        self.formatter = tk.Button(self.button_frame, text='Format/Reset', relief='raised', command=self.formatUI)
        self.popup_button = tk.Button(self.button_frame, text='Pop_out', relief='raised',
                                      command=lambda: self.pop_out_window(self.get_text()))
        self.clear = tk.Button(self.button_frame, text='Clear', relief='raised', command=self.clear_textbox)
        self.entry_button = tk.Button(self.button_frame, text='Enter Manually', relief='raised', command=self.entry)
        self.copy_button = tk.Button(self.button_frame, text='Copy', relief='raised', command=self.copy)
        self.execute_button = tk.Button(self.button_frame, text='Execute', relief='raised', command=self.execute)

        self.scroll.config(command=self.textbox.yview)

        self.formatter.grid(row=0, column=0, padx=2)
        self.popup_button.grid(row=0,  column=1, padx=2)
        self.clear.grid(row=0, column=2, padx=2)
        self.entry_button.grid(row=0, column=3, padx=2)
        self.copy_button.grid(row=0, column=4, padx=2)
        self.execute_button.grid(row=0, column=5, padx=2)

        self.button_frame.grid(row=1, sticky='w', padx=10, pady=2)

        self.textbox.grid(row=2, column=0, padx=10, pady=3, sticky='ew')
        self.scroll.grid(row=2, column=1, sticky='ns')
        self.labelframe.grid(row=row, column=col, sticky='nsew', padx=18, pady=5)
        self.formatted = False
        self.execute_command = None
        self.pool = None
        self.message = queue.Queue()
        self.t1 = None

    def get_text(self):
        return self.textbox.get("1.0", "end").strip("\n").strip(" ")

    def argument_parser(self, argument, indent):
        argument = argument.replace("'", '"').replace('\t', '').replace('\n', '').replace(',}', '}').replace(',]', ']')
        argument = argument.replace("\\", "/")
        argument = json.loads(argument)
        argument = json.dumps(argument, indent=indent)
        argument = argument.replace('"', "'")
        return argument

    def formatUI(self):
        text = self.get_text().replace('"', "")
        if text == '':
            messagebox.askokcancel("Oops", "Can't format a empty string?")
            return
        formatted = self.format(text)
        self.clear_textbox()
        self.textbox.insert(tk.INSERT, formatted)
        self.formatted = ~self.formatted


    def format(self, text):
        # try:
        pyCommand = self.text_box_info['python_command_path']
        search = 'AutomationProcessor.py'
        idx = text.find(search, len(pyCommand))
        filepath = text[len(pyCommand):idx + len(search)].strip(' ')
        dir_idx = text.find('{', len(filepath) + len(pyCommand))
        dir_ = text[idx + len(search):dir_idx].strip(' ')
        if not self.formatted:
            arguments = self.argument_parser(text[dir_idx:], 2)
        else:
            arguments = self.argument_parser(text[dir_idx:], 0)
            arguments = arguments.replace('\n', '').replace(' ', '')
        return pyCommand + ' ' + filepath + ' ' + dir_ + ' ' + arguments
        # except Exception as e:
        #     print('Exception maybe the string is empty or doesn\'t meet the standard. Find me.! :)')
        #     print(e)

    def copy(self):
        pyperclip.copy(self.get_text())

    def clear_textbox(self):
        self.textbox.delete("1.0", "end")

    def pop_out_window(self, text_msg):
        def update_main_frame():
            self.clear_textbox()
            self.textbox.insert(tk.INSERT, textbox_obj.textbox.get("1.0", "end-1c"))

        def close():
            self.master.deiconify()
            self.master.state("zoomed")
            root.destroy()


        self.master.withdraw()
        root = tk.Tk()
        root.wm_title("Pop-Up")
        textbox_obj = textBox(root, label=self.label, width=130, height=35)
        textbox_obj.formatted = self.formatted
        textbox_obj.text_box_info = self.text_box_info
        textbox_obj.textbox.insert(tk.INSERT, text_msg)
        # textbox_obj.execute_button['state'] = self.execute_button['state']
        textbox_obj.popup_button.config(text='Update', command=update_main_frame)
        textbox_obj.entry_button.grid_forget()
        textbox_obj.execute_button.config(text='Done', command=close)
        root.protocol("WM_DELETE_WINDOW", close)
        root.resizable(0, 0)
        root.mainloop()


    def get_top_line(self):
        auto_prepro_file = 'ai_datasciences_python/com/highradius/ml_automation/core/AutomationProcessor.py'
        query = self.text_box_info['python_command_path']+ ' ' + os.path.join(self.text_box_info['ai_datascience'], auto_prepro_file) + ' ' + \
                os.path.join(self.text_box_info['ai_datascience'], 'ai_datasciences_python') + ' {'
        return query

    def retrive_entry(self, info):
        self.text_box_info[self.label+"_object_list"] = info
        dump_data(self.label+"_object_list", info, self.text_box_info)
        self.make_command()


    def remove_key(self, _dict, key):
        del _dict[key]
        
    def remove_frame(self, add, _dict, frame):
        self.remove_key(_dict, add.cget("text"))
        frame.grid_forget()

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
                if entry_arguments.get() == '' or entry_python_function.get() == '' or entry_shortname.get() == '':
                    messagebox.askokcancel("Alert", "Umm.. Some fields are empty please check")
                    return

                if revisit and entry_shortname.get() != add.cget('text'):
                    self.remove_key(info, add.cget('text'))

                info[entry_shortname.get()] = {}
                info[entry_shortname.get()]['function'] = entry_python_function.get().replace("#", ".")
                info[entry_shortname.get()]['arguments'] = entry_arguments.get()
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
            #
            entry_shortname = tk.Entry(lbl_frm, width=50)
            entry_shortname.focus_set()
            entry_python_function = tk.Entry(lbl_frm, width=50)
            entry_arguments = tk.Entry(lbl_frm, width=50)
            #
            if revisit:
                set_val(entry_shortname, add.cget("text"))
                set_val(entry_python_function, info[add.cget("text")]['function'])
                set_val(entry_arguments, info[add.cget("text")]['arguments'])
            #
            entry_shortname.grid(row=0, column=1, padx=5, pady=5)
            entry_python_function.grid(row=1, column=1, padx=5, pady=5)
            entry_arguments.grid(row=2, column=1, padx=5, pady=5)
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
        pass

    def make_work(self):
        if self.label == "preprocessing" or self.label == "model_predictors":
            return (self.execute_command, )
        work = ()
        start, end = self.execute_command.find("["), self.execute_command.rfind("]")
        for string in re.findall(r"{(.*?)}", self.execute_command[start:end]):
            work += (self.execute_command[:start+1] + "{" + string + "}" + self.execute_command[end:], )
        return work

    def execute_command_f(self):
        work = self.make_work()
        outputs = []
        for w in work:
            output = subprocess.Popen(w, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            outputs.append(output)
        while any([output.poll() is None for output in outputs]):
            pass
        msg = ""
        for output in outputs:
            output = output.communicate()[0]
            output = output.decode("utf-8").strip()
            try:
                output = self.argument_parser(output, 1)
            except:
                pass
            msg += output + "\n"
        self.message.put_nowait(msg)

    def show_message(self):
        # for msg in self.message:
        #     messagebox.askokcancel("Report", msg)
        #     self.message.remove(msg)
        # self.message = []
        while self.message.qsize():
            msg = self.message.get_nowait() + "\n"
            messagebox.askokcancel("Report", msg)


    def execute(self):
        self.execute_button['state'] = 'disabled'
        if self.formatted:
            self.formatUI()

        self.execute_command = self.get_text()
        if len(self.execute_command.split(' ')) != 4 or self.formatted:
            self.execute_button['state'] = 'active'
            messagebox.askokcancel("Alert", "Texbox is empty or incorrect Gee hmm..?")
            raise Exception("Something is Fishy in your query, GEE, find me :_)")

        try:
            self.t1 = threading.Thread(target=self.execute_command_f)
            # self.t1.daemon = True
            self.t1.start()

        except Exception as e:
            print(e)
            self.execute_button['state'] = 'active'


    # def execute(self):
    #     self.execute_button['state'] = 'disabled'
    #     if self.formatted:
    #         self.formatUI()
    #
    #     self.execute_command = self.get_text()
    #     if len(self.execute_command.split(' ')) != 4 or self.formatted:
    #         self.execute_button['state'] = 'active'
    #         messagebox.askokcancel("Alert", "Texbox is empty?")
    #         raise Exception("Something is Fishy in your query, GEE, find me :_)")
    #
    #     work = self.make_work()
    #     try:
    #         self.pool = ()
    #         for w in work:
    #             p = multiprocessing.Process(target=os.system, args=(w,))
    #             p.start()
    #             self.pool += (p, )
    #
    #     except Exception as e:
    #         print(e)
    #         self.execute_button['state'] = 'active'

    def destry_process(self):
        pass







