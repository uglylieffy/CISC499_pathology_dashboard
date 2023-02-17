import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import random


filePath = 'CAP_and_LIS_Case_Views.xlsx'
# read excel file into DataFrame form 
rawDF=pd.read_excel(filePath, sheet_name='vwEccProperties_ListItem',header=0, skiprows =range(1,672), nrows=83)
# check if the read is correct and precise, from row 674-755
# print(rawDF.head(n=10))
# print(rawDF.tail(n=10))
# print(rawDF.head())

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

# # check if dictionary worked 
# for x in map_of_features:
#     print(x,':', map_of_features[x])

# Assign numerical and categorical data with their possible solution
map_of_selection = {}
for i in questionText:
    query1 = "ListItemQuestionText=='"+i+"'"
    # print(query1)
    df = rawDF.query(query1)["ListItemText"]
    # print(df)
    map_of_selection[i] = df
# tailor unecessary info 
map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)#'] = map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)#'].drop([0])
map_of_selection['Pathologic Stage Classification'] = map_of_selection['Pathologic Stage Classification'].drop([10])
map_of_selection['Regional Lymph Nodes (pN)'] = map_of_selection['Regional Lymph Nodes (pN)'].drop([34])
map_of_selection['Distant Metastasis (pM) (applicable for excision only)'] = map_of_selection['Distant Metastasis (pM) (applicable for excision only)'].drop([52])

# # check
# for x in map_of_selection:
#     print(x,':\n', map_of_selection[x],'\n')

data = []
data_header = ['patient']
data_header = data_header + num_C + cat_C
# numerical data requires 2 levels of generating data, 1st is the number
# second is the option, such as "Specify in Millimeters (mm)","At least in Millimeters (mm)","Cannot be determined (explain)"
for i in range(1,501):
    patient_name = "patient " + str(i)
    temp_list = [patient_name]
    for j in num_C:
        r1 = random.randint(0, 15)
        random_selection = map_of_selection[j].sample()
        temp_val = ((str(random_selection).split('  ')[2]).split('\n')[0]) + " - " + str(r1)
        if 'Cannot be determined' in temp_val:
            temp_list.append(((str(random_selection).split('  ')[2]).split('\n')[0]))
        else:
            temp_list.append(temp_val)
        # # if only want numbers 
        # temp_list.append(r1)
    for k in cat_C:
        random_selection = map_of_selection[k].sample()
        temp_val = ((str(random_selection).split('  ')[2]).split('\n')[0])
        temp_list.append(temp_val)
    data.append(temp_list)

# # check
# for i in data:
#     print(i, end='\n')
# print(data_header)

# generate dataframe based on the list 
patient_df = pd.DataFrame(data, columns=data_header)
# print(patient_df)

# turn to csv file 
patient_df.to_csv('fake_data.csv', index=False)
    
# visulization data 

# BAR CHART 
# fig = plt.figure()
# ax = fig.add_subplot(111)
# plt.title("Size of Largest Metastatic Deposit in Millimeters (mm)#")
# langs = ['0-3', '3-5', 'Above 5']
# students = [23,17,35]
# ax.bar(langs,students)
# plt.show()


# SCATTER PLOT 
# x = np.array([5,7,8,7,2,17,2,9,4,11,12,9,6])
# y = np.array([99,86,87,88,111,86,103,87,94,78,77,85,86])
# # plt.title("Tumor Deposits (Note G)")
# plt.scatter(x, y)
# plt.show()


# DONUT char 
# # Setting labels for items in Chart
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
# plt.pie(Salary, colors=colors, labels=Employee,
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