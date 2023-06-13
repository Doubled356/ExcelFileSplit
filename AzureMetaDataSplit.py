


import pandas as pd
import os
import glob
from os import listdir



path = "D:\\AzureMetaData\\" #directory where CSV's for splitting are stored

def find_csv_filenames (path, suffix='.csv'):
    filenames = listdir(path)
    return [filename for filename in filenames if filename.endswith(suffix)]

filenames = find_csv_filenames(path) #all csv files in directory

filelist = []

for name in filenames: #builds a list of all the csv files in the directory
    filelist.append(name)

filelist = [s.replace('.csv','') for s in filelist] #removes .csv to mimic folder names in path folder

for csvname in filelist: #loop through each file in list
    df = pd.read_csv(r'D:\\AzureMetaData\\'+ csvname + '.csv') #read the data from the csv
    df.to_excel(r'D:\\AzureMetaData\\'+ csvname + '.xlsx', index=None, header=True) #convert the csv to excel
    dfexcel = pd.read_excel('D:\\AzureMetaData\\'+ csvname + '.xlsx') #read the excel data
    column_name = dfexcel.columns[0] #set the first column as the unique values to be split
    unique_values = dfexcel[column_name].unique() #calculate how many unique values are in the table

    for unique_value in unique_values: #for each unique value in the table build an individual excel file
        df_output = df[df[column_name].str.contains(unique_value)]
        output_path = os.path.join(os.getcwd(), 'D:\\AzureMetaData\\'+csvname+'\\'+csvname+'_'+ str(unique_value) + '.xlsx')
        df_output.to_excel(output_path, sheet_name=unique_value, index=False)
        df_output.to_csv('D:\\AzureMetaData\\'+csvname+'\\'+csvname+'_'+ str(unique_value) + '.csv', index = None, header = True) # convert each excel file to csv

    for f in glob.iglob(path+'/**/*.xlsx', recursive=True): #delete the created excel files
        os.remove(f)