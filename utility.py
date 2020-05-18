from tkinter import filedialog, messagebox
import pickle
import os

def set_val(widget, text):
    widget.delete(0, "end")
    widget.insert(0, text)


def get_dir(widget):
    path_text = filedialog.askdirectory()
    set_val(widget, path_text)


def get_file(widget):
    path_text = filedialog.askopenfilename()
    set_val(widget, path_text)

def dump_data(key, val, _dict_):
    file=open(os.path.join(_dict_['dump_path'],  _dict_['account_name'] + '_info.pickle'),
                'rb')
    data = pickle.load(file)
    file.close()
    file=open(os.path.join(_dict_['dump_path'],  _dict_['account_name'] + '_info.pickle'),
                'wb')
    data[key] = val
    pickle.dump(data, file)
    file.close()

def get_data(key, _dict_):
    file=open(os.path.join(_dict_['dump_path'],  _dict_['account_name'] + '_info.pickle'),
                'rb')
    data = pickle.load(file)
    file.close()
    if key in data.keys(): return data[key]
    return None