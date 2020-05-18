from TextBox import textBox
import os
from utility import *
import tkinter as tk

class modelpredictor(textBox):

    def __init__(self, master, row=0, col=0, label='My Label', width=70, height=15):
        super().__init__(master, row, col, label, width, height)


    def make_command(self):
        if 'aggregate_file_paths' not in self.text_box_info.keys():
            val = get_data("aggregate_file_paths", self.text_box_info)
            if val is not None: self.text_box_info['aggregate_file_paths'] = val
            else:
                messagebox.askokcancel("Alert", "Didn't find any aggregation path keys please configure "
                                            "aggregation module or find me :)")
                return

        if 'model_paths' not in self.text_box_info.keys():
            val = get_data("model_paths", self.text_box_info)
            if val is not None: self.text_box_info['aggregate_file_paths'] = val
            else:
                messagebox.askokcancel("Alert", "Didn't find any aggregation path keys please configure "
                                            "aggregation module or find me :)")
                return

        cmd = self.get_top_line()
        pred_dir = os.path.join(self.text_box_info['master_path'], 'Prediction')
        preprocessed_file_path = os.path.join(os.path.join(self.text_box_info['master_path'],
                                                                                 'PreProcessed'), 'preprocessed.csv')
        cmd += "'preprocessed_file_path':'"+preprocessed_file_path+"',"
        cmd += "'aggregate_file_paths':'" + self.text_box_info['aggregate_file_paths'] + "',"
        cmd += "'raw_testing_file_path':'"+ self.text_box_info['raw_csv_path'] + "',"
        _key_ = self.label+"_object_list"
        _dict_ = self.text_box_info[_key_]
        _id_ = 1
        pred_path = ''
        cmd += "'"+_key_+"':["
        for key, val in _dict_.items():
            cmd += "{'python_function':'" + val['function'] + "',"
            cmd += "'model_file_paths':'" + self.text_box_info['model_paths'] + "',"
            pred_path += os.path.join(pred_dir, "predictions" + str(_id_) + ".csv")
            cmd += "'target_file_path':'" + os.path.join(pred_dir, "predictions" + str(_id_) + ".csv") + "',"
            cmd += "'task_shortname':'" + key + "',"
            cmd += "'task_id':'" + str(_id_) + "',"
            cmd += "'arguments':'" + val['arguments'] + "'},"
            _id_ += 1
        cmd += "],}"
        cmd = cmd.replace("\\", "/")

        dump_data('prediction_cmd', cmd, self.text_box_info)
        dump_data('pred_path', pred_path, self.text_box_info)

        self.clear_textbox()
        self.textbox.insert(tk.INSERT, cmd)
        self.formatted = False
