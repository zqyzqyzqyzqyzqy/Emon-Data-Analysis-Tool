#!/usr/bin/env python
# coding: utf-8
import sys
import pandas as pd
import math
import numpy as np
from os import listdir
from os.path import isfile, join

class DataAnanysisTool:
    def __init__(self,input_file_list,output_file,input_file):
        self.input_file_list = input_file_list
        self.output_file = output_file
        self.input_file = input_file
        
        
    def merge_data(self):
        # read file into data frame
        df_list = []
        parameter_list = []
        for f in self.input_file_list:
            data = pd.read_excel(self.input_file+'/'+f,sheet_name='system view')
            column_ls = list(data.columns)
            data_cleaned = data.drop(column_ls[2:],axis = 1)
            df_list.append(data_cleaned)
            parameter_list.append(column_ls[0])
        
        new_df = pd.merge(df_list[0], df_list[1], left_on = parameter_list[0], right_on = parameter_list[1], how = 'outer')
        #new_df.to_excel(self.output_file+"/new view.xlsx", sheet_name = 'system view',index =False)
        return new_df

    def difference_calculator(self,new_df):
        
        left_value = new_df['aggregated_x']
        right_value = new_df['aggregated_y']
        label_list = []
        for i in range(len(left_value)):
            if str(left_value[i]) == 'nan' or str(right_value[i]) == 'nan':
                label_list.append('Uncaptured Data')
            elif (max(left_value[i],right_value[i])-min(left_value[i],right_value[i]))/(min(left_value[i],right_value[i])+0.0000000001)>0.05:
                label_list.append('Difference Larger than 5%')
            else:
                label_list.append('')
        new_df['Label'] = label_list
        new_df.to_excel(self.output_file+"/new view.xlsx", sheet_name = 'system view',index =False)
    
    def excel_generator(self):
        new_df = self.merge_data()
        data_result = self.difference_calculator(new_df)
        return data_result


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = str(sys.argv[2])
    

    input_file_list = [f for f in listdir(input_file) if isfile(join(input_file, f))]


    data_analysis_tool = DataAnanysisTool(
        input_file_list = input_file_list,
        output_file = output_file,
        input_file = input_file
        )
    
    data_analysis_tool.excel_generator()
