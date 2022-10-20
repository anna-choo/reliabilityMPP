import os, collections, sys, re
import pandas as pd
import numpy as np
from openpyxl import Workbook


sys.path.insert(0, r'C:\Users\Administrator\Documents\gitHub\reliabilityMPP')

from utils.folders import OPEN_func
from sandbox.test_clean_metafile import MetaFile

class reliability_files(OPEN_func, MetaFile):
    def __init__(self, start = None, end =  None, data_initials = 'SN', change_metafile_path = None):
        super().__init__(change_metafile_path = change_metafile_path, data_initials = data_initials)

        data_list  = pd.DataFrame()
        folders = self.open_folder(self.dir)
        MPP_dir_list, MPP_list = self.open_second_folder_layer(folders)
        self.folder_path_list = self.get_folder_path(MPP_dir_list)
        
    # def RENAME_files(self):
        for i, j in self.folder_path_list.items():
            for k in j:
                df, error = self.get_cleaned_data_only(start = i, change_metafile_path = r"{}".format(k))
                for index, row in df.iterrows():
                    self.rename_func(path = os.path.join(k, "v2"), subjectNumber=i, file_id = row['file id'], new_name = row['file name'], file_type = 'qtm')
    
                    
        



if __name__ == "__main__":
    test = RENAME_files()