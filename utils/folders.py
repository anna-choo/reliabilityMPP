# import imp
import os, collections, sys, re
import pandas as pd
import numpy as np
from openpyxl import Workbook
# from sympy import im

sys.path.insert(0, r'C:\Users\Administrator\Documents\gitHub\reliabilityMPP')

from init import GLOBAL

class OPEN_func(GLOBAL):
    def __init__(self, **kw):
        super().__init__(**kw)
        # print("bye")

    def open_folder(self, folder_to_open):
        file_list = []
        for files in os.listdir(folder_to_open):
            file_list.append(files)
        return file_list
    
    def open_second_folder_layer(self, list_of_folders):
        folders = self.open_folder(self.dir)
        MPP_list = []
        MPP_dir_list = collections.defaultdict(list)
        for date in folders:
            MPP = self.open_folder(os.path.join(self.dir, date, self.secondLayer_dir))
            MPP_dir_list[date] = MPP
            MPP_list.extend(MPP)
        return MPP_dir_list, MPP_list

    def get_folder_path(self, MPP_list):
        folder_path_list = collections.defaultdict(list)
        for dates, MPPs in MPP_list.items():
            for MPP in MPPs:
                folder_path_list[MPP].append(os.path.join(self.dir, dates, self.secondLayer_dir, MPP))
        return folder_path_list


    def rename_func(self, path, subjectNumber, file_id, new_name, file_type):
        old_name = str(subjectNumber) + '_' +  str(file_id).zfill(4) + '.' + str(file_type)
        new_name = new_name + '.' + str(file_type)
        os.rename(os.path.join(path,old_name), os.path.join(path, new_name))
    

