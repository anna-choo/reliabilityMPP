import os, collections, sys, re
import pandas as pd
import numpy as np
from openpyxl import Workbook


sys.path.insert(0, r'C:\Users\Administrator\Documents\gitHub\dataRequest')

from init import GLOBAL

class MetaFile(GLOBAL):
    
    VERSION = '1.0'
    def __init__(self, change_metafile_path = None, data_initials = 'SN', **kw):
        super().__init__(**kw)

        # change path and data initials if requirement stated
        self.change_metafile_path = change_metafile_path
        self.data_initials = data_initials
        self.error_list = collections.defaultdict(list)
        self.history = []

    ####################
    # call this function to append mega metafile
    ####################
    
    def update_mega_metafile(self, start = None, end = None, append_to_mega_meta = False, change_metafile_path = None):
        self.subject(start, end)       # generate self.subject_list
        self.set_up_for_mega_metafile()
        self.standard_procedure(append_to_mega_meta, change_metafile_path)

        return self.cleaned_data, self.error_list

    ####################
    # this function is to get  details in metafiles only
    ####################

    def get_cleaned_data_only(self, start = None, end = None, append_to_mega_meta = False, change_metafile_path = None):
        print(change_metafile_path)
        self.subject(start, end)       # generate self.subject_list
        self.standard_procedure(append_to_mega_meta, change_metafile_path)
        return self.cleaned_data, self.error_list


    ##########################################################################################
    # operation wise functions

    ####################
    # load mega metafile
    ####################                       
    def set_up_for_mega_metafile(self):
        self.mega_metafile_path = os.path.join(self.MEGA_METAFILE_DIR, self.mega_metafile)
        
        # check if subject metafile has already been recorded in mega metafile
        if os.path.exists(self.mega_metafile_path):
            self.success_mega_meta_workbook = pd.read_excel(self.mega_metafile_path, sheet_name = 'successful trials')
            self.discarded_mega_meta_workbook = pd.read_excel(self.mega_metafile_path, sheet_name = 'discarded trials')
            self.history = list((np.unique(self.success_mega_meta_workbook['subject number'])))
            


    ####################
    # check header and transform
    ####################
    def standard_procedure(self, append_to_metafile = False, change_metafile_path = None):
        print('path:', change_metafile_path)
        self.cleaned_data = pd.DataFrame()
        for subjectNumber in self.subject_list:
            print("start", subjectNumber)
            
            main_header = [self.VERSION, subjectNumber, 'dom', 'stronghand', 'strongleg', 'video' ]
            sub_header = ['file id', 'task', 'hand/leg', 'trial #', 'trial fail #', 'sensor fail #', 'remarks']
            self.load_file(subjectNumber, change_metafile_path)

            # check version
            self.check_version(subjectNumber)
            if subjectNumber in self.error_list:
                print("error for", subjectNumber, ":", self.error_list[subjectNumber])
                continue
            else:
                # check header
                co_header = self.check_header(main_header, sub_header, subjectNumber)
                if subjectNumber in self.error_list:
                    print("error for", subjectNumber, ":", self.error_list[subjectNumber])
                    continue
                else:
                    self.transform(subjectNumber, sub_header, co_header)
                    self.task = self.raw['task']
                    self.failed_trials = self.raw['trial fail #']
                    self.separate_data()
                    self.task = self.successful_trials['task']      #re-define
                    self.side = self.successful_trials['hand/leg']
                    self.file_id = self.successful_trials['file id']
                    self.create_file_name(subjectNumber)
                    if subjectNumber in self.error_list:
                        print("error for", subjectNumber, ":", self.error_list[subjectNumber])
                        continue
                    else:
                        self.cleaned_data = pd.concat([self.cleaned_data, self.successful_trials], axis = 0)
                        if append_to_metafile:
                            if subjectNumber in self.history:
                                print(subjectNumber, "record is already in mega metafile!")
                                print("done for:", subjectNumber)
                                continue
                        
                        # if not os.path.exists(self.mega_metafile_path):
                        #     self
                        #     self.save_to_mega_metafile()
                        #     print("done for:", subjectNumber)
                        # else:
                        self.compile_mega_metafile()
                        self.save_to_mega_metafile()
                        print("done for:", subjectNumber)

    

    ####################
    # save file
    ####################
    def save_to_mega_metafile(self):
        writer = pd.ExcelWriter(self.mega_metafile_path, engine = 'xlsxwriter')
        self.success_mega_meta_workbook.to_excel(writer, sheet_name = 'successful trials', index = False)
        self.discarded_mega_meta_workbook.to_excel(writer, sheet_name = 'discarded trials', index = False)
        writer.save()
        writer.close()
            

            




                
            



    ####################
    # determine the subject
    ####################
    def subject(self, start = None, end = None):
        self.subject_list = []
        if start is None and end is None:
            self.subject_list = "input error, no subject number is selected"
        elif isinstance(start, str):
            self.subject_list.append(start)
        elif start == 0:
            self.subject_list = "input error, no subject number starts from 0"
        elif end is not None and start>end:
            self.subject_list =  "input error, starting number is larger than ending number"
        elif isinstance(start, int):
            if not end:
                end = start
            for i in range(start, end + 1):
                self.subject_list.append(str(self.data_initials) + str(i).zfill(self.number_filler))
        elif isinstance(start, list) and end is None:
            self.subject_list = start
        elif isinstance(start, list) and end is not None:
            self.subject_list =  "input error"
        
        
    

    ####################
    # load file
    ####################
    def load_file(self, subjectNumber, change_metafile_path):
        if change_metafile_path is None:
            self.raw = pd.read_excel(os.path.join(self.metafile_path, "meta files - " + subjectNumber + ".xlsx"))
        else:
            self.raw = pd.read_excel(os.path.join(change_metafile_path, "meta files - " + subjectNumber + ".xlsx"))

        
        
    ####################
    # check if version of metafile is correct
    # ####################
    def check_version(self, subjectNumber):
        if self.VERSION != self.raw.columns[0]:
            # sound out if version does not tally
            self.error_list[subjectNumber].append("check version")



    ####################
    # standardize metafile header structure and also check for subject number stated in the meta file
    ####################
    def check_header(self, main_header, sub_header, subjectNumber):
        
        # exclude headers that dont have anything
        # original_header =  self.raw.columns.str.contains('^Unnamed')]
        original_header = self.raw.columns[~self.raw.columns.str.contains('^Unnamed')]


       # check if structure of main header is correct
        if len(main_header) >= len(original_header):
            for i in range(len(original_header)):
                if not original_header[i][:len(main_header[i])].lower().strip() == main_header[i].lower():
                    self.error_list[subjectNumber].append(original_header[i])

        elif len(main_header) < len(original_header):
            for i in range(len(main_header)):
                if not original_header[i][:len(main_header[i])].lower().strip() == main_header[i].lower():
                    self.error_list[subjectNumber].append(original_header[i])
        
        # # except:
        #     # self.error_list[subjectNumber].append("original header")

        # stop if main header is wrong
        if subjectNumber in self.error_list:
            return


        else:
            # grab sub header 
            co_header = self.raw[self.raw[self.VERSION] == sub_header[0]].index[0]
            self.raw.columns = self.raw.iloc[co_header]
            self.raw.columns = [str(i).strip().lower() for i in self.raw.columns]
        
            # check if sub header is correct
            for i in range(len(sub_header)):
                if self.raw.columns[i] != sub_header[i]:
                    self.error_list[subjectNumber].append(self.raw.columns[i])
            return co_header


        


        
    ####################
    # check content of metafile (not done)
    ####################
    def check_content(self):
        
        ## anyway other way to do this so that can edit in init??
        # to set parameters for metafile
        task = self.raw["task"]
        side = self.raw["hand/leg"]
        file_id = self.raw["file id"]
        repetition = self.raw["trial #"]

        # print(discard)

        file_id_list = collections.defaultdict(list)

        for i in self.task_list:
            
            for j in self.task_list[i]:
                file_id_list[i].extend(file_id[task == j])

        # print(data_initials(accept["file id"]))
        # print(file_id_list)
        # print(accept)
        # print(np.where([accept["file id"] == id for id in file_id_list["unilateral"]]))
        for id in file_id_list["unilateral"]:
            #     # print(accept[accept["file id"] == id]["trial #"])
        # #     print(accept["task"][int(id)])
        #     print(accept["trial #"][accept["file id"] == id])
        #     print(accept.loc[int(id), "trial #"])
            for a in accept["trial #"][accept["file id"] == id]:
                print(a)
                y = re.findall(r'[A-z]*',a)
                print(y)

                # print(a)
                # if not check:
                #     print(check)
                # print(check) 
            # print(accept["trial #"][accept["file id"] == id])
            # find = re.match(r'[0-9]*-{0,1}[0-9]*', accepted_repetition)
            # print(accepted_repetition)

        #     print(repetition[int(i)])


        
        
        # if discard = "ALL"
        # print(task)
        # print(self.raw[task] in self.task_list["unilateral"])
        # for unilateral_task in self.unilateral:
        #     if side[task == unilateral_task] == "L":
                
        # print(self.raw)
        # trial = self.raw["trial #"]



    ####################
    # cleaning up data
    ####################
    def transform(self, subjectNumber, sub_header, co_header):
        
        # exclude any columns that is not supposed to be inside
        self.raw = self.raw[self.raw.columns.intersection(sub_header)]

        # change header to sub header
        self.raw.drop([i for i in range(co_header + 1)], inplace = True)
        self.raw = self.raw.reset_index(drop = True)
        self.raw.columns.name = None

        # # drop rows if all empty
        self.raw = self.raw.replace(['^\s+$'], np.nan, regex = True)
        self.raw = self.raw.dropna(how='all')

        # # # # clear up whitespaces
        self.raw = self.raw.astype(str)
        self.raw = self.raw.apply(lambda x: x.str.strip())
        self.raw["task"] = self.raw["task"].apply(lambda x: x.lower())
        # print(self.raw)

        ## is there any way to code this on top? 
        self.raw['file id'] = (self.raw['file id'].astype(float)).astype(int)


        # insert subject number
        self.raw.insert(0, 'subject number', subjectNumber)


    ####################
    # split into success and discard
    ####################
    def separate_data(self):
            # check both condition that it's not old task and is not discarded task
            boolean_df = pd.concat([np.logical_not(self.task.isin(self.task_list['ignore_task'])), self.failed_trials != "ALL" ], axis = 1)
            self.raw["include"] = boolean_df.sum(axis=1)
            # take relevant data
            self.successful_trials = self.raw[self.raw["include"] == 2]
            del self.successful_trials["include"]
            self.discarded_trials = self.raw[self.raw["include"] != 2]
            del self.discarded_trials["include"]
            del self.raw["include"]



    ####################
    # determine the file name for each task
    ####################    
    def create_file_name(self, subjectNumber):
        file_name_list = []
        counter = {}

        for i in range(len(self.successful_trials)):
            # print(self.task.iloc[i])
            if self.task.iloc[i] in self.task_list['unilateral']:
                counter_name = self.task.iloc[i] + self.side.iloc[i]
            elif self.task.iloc[i] in self.task_list['bilateral']:
                counter_name = self.task.iloc[i]
            else:
                self.error_list[subjectNumber].append(self.task.iloc[i])
                return

            if counter_name not in counter:
                counter[counter_name] = 1
            else:
                counter[counter_name] += 1

            if self.task.iloc[i] in self.task_list['unilateral']:
                file_name = subjectNumber + '_' + str(self.file_id.iloc[i]).zfill(4) + '_' + str(self.task.iloc[i]) + '_' + str(self.side.iloc[i]) + str(counter[counter_name]).zfill(2)
            elif self.task.iloc[i] in self.task_list['bilateral']:
                counter_name = self.task.iloc[i]
                file_name = subjectNumber + '_' + str(self.file_id.iloc[i]).zfill(4) + '_' + str(self.task.iloc[i]) + '_' + str(counter[counter_name]).zfill(2)

            file_name_list.append(file_name)

        # record into dataframe
        self.successful_trials['file name'] = file_name_list
        
            # print(file_name)
            

    
    ####################
    # print into different mega metafile
    ####################
    def compile_mega_metafile(self):
        
        if os.path.exists(self.mega_metafile_path):
            self.success_mega_meta_workbook = pd.concat([self.success_mega_meta_workbook, self.successful_trials], axis = 0)
            self.discarded_mega_meta_workbook = pd.concat([self.discarded_mega_meta_workbook, self.discarded_trials], axis = 0)
        else:
            self.success_mega_meta_workbook = self.successful_trials
            self.discarded_mega_meta_workbook = self.discarded_trials
            

if __name__ == "__main__":
    test = MetaFile()
    test.update_mega_metafile(1,3, append_to_mega_meta= True)
