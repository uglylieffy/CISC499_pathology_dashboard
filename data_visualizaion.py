import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.cm as cm
import seaborn
import math


def data_generator(num):
    filePath = 'CAP_and_LIS_Case_Views.xlsx'
    # read excel file into DataFrame form 
    rawDF=pd.read_excel(filePath, sheet_name='vwEccProperties_ListItem',header=0, skiprows =range(1,672), nrows=83)


    # extract all unqie col C
    questionText = rawDF['ListItemQuestionText'].unique().tolist()
    # print(len(questionText))

    # generate a dictionary for storing datatype, categorical or numerical 
    map_of_features  = {}
    # numerical Col C names 
    num_C = ['Size of Largest Metastatic Deposit in Millimeters (mm)#',
            'Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)', 
            'Distance of Melanoma in situ from Deep Margin in Millimeters (mm)', 
            'Distance of Invasive Melanoma from Closest Peripheral Margin in Millimeters (mm)',
            'Distance of Invasive Melanoma from Deep Margin in Millimeters (mm)', 
            'Number of Lymph Nodes with Tumor', 'Tumor Size']
    for i in num_C:
        map_of_features[i] = "N"
    # generate categorical list based on the numerical list 
    # cat_C = list(set(num_C).symmetric_difference(set(questionText)))
    # cat_C = list(set(questionText) - set(num_C))
    cat_C = [i for i in questionText if i not in num_C]
    # print(len(cat_C))
    for i in cat_C:
        map_of_features[i] = "C"

    # Assign numerical and categorical data with their possible solution
    map_of_selection = {}
    for i in questionText:
        query1 = "ListItemQuestionText=='"+i+"'"
        # print(query1)
        df = rawDF.query(query1)["ListItemText"]
        # print(df)
        if i == 'Size of Largest Metastatic Deposit in Millimeters (mm)#':
            map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)'] = df
            num_C = list(map(lambda x: x.replace('Size of Largest Metastatic Deposit in Millimeters (mm)#', 'Size of Largest Metastatic Deposit in Millimeters (mm)'), num_C))
        elif i == 'Distant Metastasis (pM) (applicable for excision only)':
            map_of_selection['Distant Metastasis (pM)'] = df
            cat_C = list(map(lambda x: x.replace('Distant Metastasis (pM) (applicable for excision only)', 'Distant Metastasis (pM)'), cat_C))
        else:
            map_of_selection[i] = df
    # tailor unecessary info 
    # Size of Largest Metastatic Deposit in Millimeters (mm)
    map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)'] = map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)'].drop([0])
    # print(map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)'])
    
    # Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)
    map_of_selection['Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)'] = map_of_selection['Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)'].drop([60,61,62])
    # print(map_of_selection['Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)'])
    
    # Primary Tumor (pT)
    for index in map_of_selection['Primary Tumor (pT)'].index:
        val = map_of_selection['Primary Tumor (pT)'][index]
        if ': ' in val:
            map_of_selection['Primary Tumor (pT)'][index] = (str(val).split(': '))[0]
        else:
            map_of_selection['Primary Tumor (pT)'] = map_of_selection['Primary Tumor (pT)'].drop([index])
    # print(map_of_selection['Primary Tumor (pT)'])

    # Regional Lymph Nodes (pN)
    map_of_selection['Regional Lymph Nodes (pN)'] = map_of_selection['Regional Lymph Nodes (pN)'].drop([34])
    for index in map_of_selection['Regional Lymph Nodes (pN)'].index:
        val = map_of_selection['Regional Lymph Nodes (pN)'][index]
        if ': ' in val:
            map_of_selection['Regional Lymph Nodes (pN)'][index] = (str(val).split(': '))[0]
        else:
            map_of_selection['Regional Lymph Nodes (pN)'] = map_of_selection['Regional Lymph Nodes (pN)'].drop([index])
    # print(map_of_selection['Regional Lymph Nodes (pN)'])

    # Distant Metastasis (pM)
    map_of_selection['Distant Metastasis (pM)'] = map_of_selection['Distant Metastasis (pM)'].drop([52])
    map_of_selection['Distant Metastasis (pM)'] = map_of_selection['Distant Metastasis (pM)'].drop([54])
    for index in map_of_selection['Distant Metastasis (pM)'].index:
        val = map_of_selection['Distant Metastasis (pM)'][index]
        if ': ' in val:
            map_of_selection['Distant Metastasis (pM)'][index] = (str(val).split(': '))[0]
        else:
            map_of_selection['Distant Metastasis (pM)'] = map_of_selection['Distant Metastasis (pM)'].drop([index])
    # print(map_of_selection['Distant Metastasis (pM)'])
        
    # Pathologic Stage Classification
    map_of_selection['TNM Descriptors'][12] = "Not applicable"
    # print(map_of_selection['TNM Descriptors'])

    # Pathologic Stage Classification
    map_of_selection['Pathologic Stage Classification'] = map_of_selection['Pathologic Stage Classification'].drop([10])
    

    data = []
    data_header = ['patient']
    data_header = data_header + num_C + cat_C
    # print(map_of_selection['Status of Melanoma In Situ at Peripheral Margins'])
    # numerical data requires 2 levels of generating data, 1st is the number
    # second is the option, such as "Specify in Millimeters (mm)","At least in Millimeters (mm)","Cannot be determined (explain)"
    for i in range(1,(num+1)):
        patient_name = "patient " + str(i)
        temp_list = [patient_name]
        for j in num_C:
            # random generated numerical value range 0-15 
            r1 = random.randint(0, 15)
            # select from the values of map_of_selection map 
            random_selection = map_of_selection[j].sample()
            temp_val = ((str(random_selection).split('  ')[2]).split('\n')[0]) + " - " + str(r1)
            if 'Cannot be determined' in temp_val:
                temp_list.append(str('Cannot be determined'))
            else:
                temp_list.append(temp_val)
            # # if only want numbers 
            # temp_list.append(r1)
        # print(temp_list)
        for k in cat_C:
            # select from the values of map_of_selection map 
            random_selection = map_of_selection[k].sample()
            temp_val = ((str(random_selection).split('  ')[2]).split('\n')[0])
            if '?Not applicable' in temp_val:
                temp_list.append(str('Not applicable'))
            elif ': ' in temp_val:
                temp_list.append(str(temp_val).split(': ')[0])
                # print("FOUNDIT")
            elif ' (' in temp_val:
                temp_list.append(str(temp_val).split(' (')[0])
            else:
                temp_list.append(temp_val)
        # print(temp_list)
        data.append(temp_list)
    # print(data)

    # # generate dataframe based on the list 
    patient_df = pd.DataFrame(data, columns=data_header)
    return patient_df

# # 1000 patients data generation
# fake_data = data_generator(100)
# # turn to csv file 
# fake_data.to_csv('fake_data.csv', index=False)
    
def split_df(path, header):
    # # import data 
    patient_df = pd.read_csv(path)    
    # clean data to be desired format 
    temp_df = patient_df[header].copy()
    for j in temp_df.index:
        val = temp_df[j]
        if ' - ' in val:
            temp_df[j] = str(val).split(' - ')[-1]
    temp_df.to_csv('temp3.csv', index=False)


# bar Chart generator ? data preparation 
def prep_singular_data(path, header):
    hist_df = pd.read_csv(path, header=0)    

    label = []
    # group df vales into 4 groups, 0-5, 5-10, 10-15, not determined 
    for i in hist_df.index:
        val = hist_df.loc[i,header]
        if str(val) != 'Cannot be determined':
            val = int(val)
            if 0 <= val < 5:
                label.append(1)
            elif 5 <= val < 10:
                label.append(2)
            else:
                label.append(3)
        else:
            label.append(4)
    # add group labelling to df 
    hist_df['Label']= label
    return hist_df


header1 = 'Size of Largest Metastatic Deposit in Millimeters (mm)'
test_df = prep_singular_data('temp.csv', header1)
# print(test_df)
header2 = 'Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)'
# split_df('fake_data.csv', header2)
test_df2 = prep_singular_data('temp2.csv', header2)
# print(test_df2)
header3 = 'Distance of Melanoma in situ from Deep Margin in Millimeters (mm)'
# split_df('fake_data.csv', header3)
test_df3 = prep_singular_data('temp3.csv', header3)

# BAR CAHRT
def bar_char(test_df):
    # calculate sum of points for each team
    unique_val = test_df['Label'].unique()
    # generate data dict to plot data 
    data = {}
    for i in unique_val:
        if i == 1:
            data['0-5'] = int(test_df['Label'].value_counts()[i])
        elif i == 2:
            data['5-10'] = int(test_df['Label'].value_counts()[i])
        elif i == 3:
            data['10-15'] = int(test_df['Label'].value_counts()[i])
        else:
            data['not determined'] = int(test_df['Label'].value_counts()[i])
    # print(data)

    # create bar plot 
    names = list(data.keys())
    counts = list(data.values())
    fig, ax = plt.subplots()
    bar_container = ax.bar(names, counts)
    ax.set(ylabel='num of patients', title=header1)
    ax.bar_label(bar_container, label_type='center')
    plt.show()
bar_char(test_df)


# SCATTER PLOT 
def scatter_plt(test_df1,test_df2,header):
    x = test_df1[header1].replace(['Cannot be determined'],-1)
    y = test_df2[header2].replace(['Cannot be determined'],-1)
    plt.title(header)
    plt.xlim([-2,16])
    plt.ylim([-2,16])
    plt.xlabel(header1)
    plt.ylabel(header2)
    plt.scatter(x, y)
    plt.show()
scatter_plt(test_df,test_df2,"Size of Largest Metastatic Deposit v.s. Distance of Melanoma in situ from Closest Peripheral Margin")

# LINE CHART
def line_char(test_df1,test_df2,test_df3,header):
    # calculate sum of points for each team
    unique_val = []
    df_list = [test_df1,test_df2,test_df3]
    # print(df_list)
    unique_val1 = test_df1['Label'].unique()
    unique_val.append(unique_val1)
    unique_val2 = test_df2['Label'].unique()
    unique_val.append(unique_val2)
    unique_val3 = test_df3['Label'].unique()
    unique_val.append(unique_val3)
    # unique_val = unique_val1+unique_val2+unique_val3
    # print(unique_val[0])

    # generate data dict to plot data 
    data = {}
    for k in range(len(unique_val)):
        for i in unique_val[k]:
            if k == 0:
                if i == 1:
                    data['0-5'] = [int(df_list[k]['Label'].value_counts()[i])]
                elif i == 2:
                    data['5-10'] = [int(df_list[k]['Label'].value_counts()[i])]
                elif i == 3:
                    data['10-15'] = [int(df_list[k]['Label'].value_counts()[i])]
                else:
                    data['not determined'] = [int(df_list[k]['Label'].value_counts()[i])]
            else:
                if i == 1:
                    data['0-5'].append(int(df_list[k]['Label'].value_counts()[i]))
                elif i == 2:
                    data['5-10'].append(int(df_list[k]['Label'].value_counts()[i]))
                elif i == 3:
                    data['10-15'].append(int(df_list[k]['Label'].value_counts()[i]))
                else:
                    data['not determined'].append(int(df_list[k]['Label'].value_counts()[i]))                 
    # print(data)

    key_list = list(data.keys())    
    for i in range(len(data[key_list[0]])):
        temp_list = []
        for value in data.values():
            temp_list.append(value[i])
            # print(temp_list)
        plt.plot(key_list, temp_list)
    plt.title(header, fontsize=12)
    plt.xlabel('result type', fontsize=12)
    plt.ylabel('number', fontsize=12)
    plt.grid(True)
    plt.show()

line_char(test_df,test_df2,test_df3,"Tendency")




# DONUT char 
# # Setting label for items in Chart
# Employee = ['No evidence of primary tumor', 'Tumor invades lamina propria or muscularis mucosa', 'Tumor invades submucosa',
#             ' Tumor invades muscularis propria', ' Cannot be assessed']
# # Setting size in Chart based on 
# # given values
# Salary = [2, 2, 2, 4, 2]
# # colors
# colors = ['#FF0000', '#0000FF', '#FFFF00', 
#           '#ADFF2F', '#FFA500']
# # explosion
# explode = (0.05, 0.05, 0.05, 0.05, 0.05)
# # Pie Chart
# plt.pie(Salary, colors=colors, label=Employee,
#         autopct='%1.1f%%', pctdistance=0.85,
#         explode=explode)
# # draw circle
# centre_circle = plt.Circle((0, 0), 0.70, fc='white')
# fig = plt.gcf()
# # Adding Circle in Pie chart
# fig.gca().add_artist(centre_circle)
# # Adding Title of chart
# plt.title('Tumor Deposits (Note G)')
# # Displaying Chart
# plt.show()