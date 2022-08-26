#Liangyz
#2022/8/16  11:51

import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
import os,glob
"""4 agent"""
Mcts_agent_1000 = 'AI(MCTS)'
Mcts_agent_50 = 'AI(MCTS_50)'
Mcts_agent_100 = 'AI(MCTS_100)'
Mcts_agent_200 = 'AI(MCTS_200)'
Mcts_agent_300 = 'AI(MCTS_300)'
Mcts_agent_400 = 'AI(MCTS_400)'
Mcts_agent_500 = 'AI(MCTS_500)'
# Mcts_agent_random = 'AI(MCTS_random)'
eva_agent = 'AI(Evaluate)'
# ,Minmax_agent_1
target_agent_list = [Mcts_agent_1000,Mcts_agent_50,Mcts_agent_100,Mcts_agent_200,Mcts_agent_300,Mcts_agent_400,Mcts_agent_500,eva_agent]#,Mcts_agent_random
"""get csv"""
file_path= "D:\\Durham\\Project\\code\\Data_collection"
folder_dir = os.listdir(file_path)
count = 0
Mcts_csv_list = []
Mcts_50_csv_list = []
Mcts_100_csv_list =[]
Mcts_200_csv_list = []
Mcts_300_csv_list = []
Mcts_400_csv_list = []
Mcts_500_csv_list = []
Mcts_1000_csv_list = []

csv_list = []

for folder in folder_dir:
    if folder in target_agent_list:
        file_dir = os.listdir(file_path + "\\" + folder)
        for file in file_dir:
            if file in target_agent_list:
            # if file is Minmax_agent_4:
                csv_path = file_path + "\\" + folder + "\\" + file + "\\" + folder + "_VS_"+ file
                # print(csv_path)
                # target_csv_path = csv_path + "\\" + folder + "_VS_" + file + "_2022-08-1" + "*.csv"
                target_csv_path = csv_path + "\\" + folder + "_VS_" + eva_agent + "_2022-08-1" + "*.csv"

                # print(target_csv_path)
                all_csv_name = glob.glob(target_csv_path)
                # all_csv_name_4 = glob.glob(target_csv_path_4)
                # all_csv_name_5 = glob.glob(target_csv_path_5)
                # all_csv_name_ab_5 = glob.glob(target_csv_path_ab_5)
                print(all_csv_name)
                if all_csv_name != []:
                    for csv_name in all_csv_name:
                        if folder == Mcts_agent_1000:
                            Mcts_1000_csv_list.append(pd.read_csv(csv_name))
                        elif folder == Mcts_agent_50:
                            Mcts_50_csv_list.append(pd.read_csv(csv_name))
                        elif folder == Mcts_agent_100:
                            Mcts_100_csv_list.append(pd.read_csv(csv_name))
                        elif folder == Mcts_agent_200:
                            Mcts_200_csv_list.append(pd.read_csv(csv_name))
                        elif folder == Mcts_agent_300:
                            Mcts_300_csv_list.append(pd.read_csv(csv_name))
                        elif folder == Mcts_agent_400:
                            Mcts_400_csv_list.append(pd.read_csv(csv_name))
                        elif folder == Mcts_agent_500:
                            Mcts_500_csv_list.append(pd.read_csv(csv_name))
                    # for csv_name in all_csv_name:
                    #     Mcts_csv_list.append(pd.read_csv(csv_name))
#
# Mcts_csv = pd.concat(Mcts_csv_list)
# print(Mcts_csv.head(0),Mcts_csv.shape)
# # print(Mcts_csv.iloc[1]['Move Time'])
# max_time_list = []
# for i in range(0,Mcts_csv.shape[0]):
#     Mcts_time_s = Mcts_csv.iloc[i]['Move Time']
#     Mcts_time = json.loads(Mcts_time_s)
#     max_time_list.append(max(Mcts_time[0]))
# print(max(max_time_list))

Mcts_50_csv = pd.concat(Mcts_50_csv_list)
Mcts_100_csv = pd.concat(Mcts_100_csv_list)
Mcts_200_csv = pd.concat(Mcts_200_csv_list)
Mcts_300_csv = pd.concat(Mcts_300_csv_list)
Mcts_400_csv = pd.concat(Mcts_400_csv_list)
Mcts_500_csv = pd.concat(Mcts_500_csv_list)
Mcts_1000_csv = pd.concat(Mcts_1000_csv_list)

print('Mcts_50')
print(Mcts_50_csv.head(0),Mcts_50_csv.shape)
print(Mcts_50_csv['Winner'].value_counts(1))
print('------------------------------')
print('Mcts_100')
print(Mcts_100_csv.head(0),Mcts_100_csv.shape)
print(Mcts_100_csv['Winner'].value_counts(1))
print('------------------------------')
print('Mcts_200')
print(Mcts_200_csv.head(0),Mcts_200_csv.shape)
print(Mcts_200_csv['Winner'].value_counts(1))
print('------------------------------')
print('Mcts_300')
print(Mcts_300_csv.head(0),Mcts_300_csv.shape)
print(Mcts_300_csv['Winner'].value_counts(1))
print('------------------------------')
print('Mcts_400')
print(Mcts_400_csv.head(0),Mcts_400_csv.shape)
print(Mcts_400_csv['Winner'].value_counts(1))
print('------------------------------')
print('Mcts_500')
print(Mcts_500_csv.head(0),Mcts_500_csv.shape)
print(Mcts_500_csv['Winner'].value_counts(1))
print('------------------------------')
print('Mcts_1000')
print(Mcts_1000_csv.head(0),Mcts_1000_csv.shape)
print(Mcts_1000_csv['Winner'].value_counts(1))

y = [Mcts_50_csv['Winner'].value_counts(1)[1],Mcts_100_csv['Winner'].value_counts(1)[1],Mcts_200_csv['Winner'].value_counts(1)[1],Mcts_300_csv['Winner'].value_counts(1)[1],Mcts_400_csv['Winner'].value_counts(1)[1],Mcts_500_csv['Winner'].value_counts(1)[1],Mcts_1000_csv['Winner'].value_counts(1)[1]]
x = [50,100,200,300,400,500,1000]
x_bar = [i for i in range(1,len(x)+1)]
y_text = [str(round(Mcts_50_csv['Winner'].value_counts(1)[1],3)),str(round(Mcts_100_csv['Winner'].value_counts(1)[1],3)),str(round(Mcts_200_csv['Winner'].value_counts(1)[1],3)),str(round(Mcts_300_csv['Winner'].value_counts(1)[1],3)),str(round(Mcts_400_csv['Winner'].value_counts(1)[1],3)),str(round(Mcts_500_csv['Winner'].value_counts(1)[1],3)),str(round(Mcts_1000_csv['Winner'].value_counts(1)[1],3))]

plt.bar(x_bar,y,width=0.8)
plt.plot(x_bar,y,'co-',linewidth=2)
for i in range(0,len(x)):
    plt.text(x_bar[i],y[i],'   ('+y_text[i]+') \n',ha='center',va='bottom',fontsize=10)
plt.xticks(x_bar,x)
plt.ylim(0.6,0.8)
plt.xlabel('Number of Loops')
plt.ylabel('Winning Rate')
plt.title('Winning Rate of MCTS Agent')
plt.grid(True,linestyle='-.',alpha=0.3)
plt.minorticks_on()
plt.savefig('MCTS_winning_rate_with_different_loops.png')
plt.show()


# plt.pie(Mcts_csv['Winner'].value_counts(1),
#         labels=['Win','Lose','Draw'],
#         autopct='%1.1f%%',
#         shadow=False,
#         startangle=270,
#         pctdistance=0.6,
#         radius=1.2,
#         labeldistance=1.1,
#         textprops={'fontsize':12},
#         explode=[0.05,0,0],)
# plt.title('Score of MCTS_Roxanne')
# plt.savefig('MCTS_Roxanne.png')
# plt.show()



                # print(all_csv_name_4)
                # print(all_csv_name_5)
                # print(all_csv_name_ab_5)
                #
                # if all_csv_name_4 != []:
                #     Minmax_agent_4_csv_list.append(pd.read_csv(all_csv_name_4[0]))
                # if all_csv_name_5 != []:
                #     Minmax_agent_5_csv_list.append(pd.read_csv(all_csv_name_5[0]))
                #
                # if all_csv_name_ab_5 != []:
                #     alpha_agent_5_csv_list.append(pd.read_csv(all_csv_name_ab_5[0]))
                # if all_csv_name != []:
                #     if count < 3:
                #         Minmax_agent_1_csv_list.append(pd.read_csv(all_csv_name[0]))
                #         count += 1
                #     elif count < 6:
                #         Minmax_agent_2_csv_list.append(pd.read_csv(all_csv_name[0]))
                #         count += 1
                #     elif count < 9:
                #         Minmax_agent_3_csv_list.append(pd.read_csv(all_csv_name[0]))
                #         count += 1
                # elif count < 12:
                #     Scmin_csv_list.append(pd.read_csv(all_csv_name[0], index_col=0))
                #     count += 1
# """1-4"""
# Minmax_agent_1_csv = pd.concat(Minmax_agent_1_csv_list)
# Minmax_agent_2_csv = pd.concat(Minmax_agent_2_csv_list)
# Minmax_agent_3_csv = pd.concat(Minmax_agent_3_csv_list)
# Minmax_agent_4_csv = pd.concat(Minmax_agent_4_csv_list)
# print('Minmax_1',Minmax_agent_1_csv.head(0),Minmax_agent_1_csv.shape)
# print(Minmax_agent_1_csv['Winner'].value_counts(1))
# print(Minmax_agent_1_csv['Winner'].value_counts(1)[1])
#
# print('Minmax_2',Minmax_agent_2_csv.head(0),Minmax_agent_2_csv.shape)
# print(Minmax_agent_2_csv['Winner'].value_counts(1))
# print(Minmax_agent_2_csv['Winner'].value_counts(1)[1])
#
# print('Minmax_3',Minmax_agent_3_csv.head(0),Minmax_agent_3_csv.shape)
# print(Minmax_agent_3_csv['Winner'].value_counts(1))
# print(Minmax_agent_3_csv['Winner'].value_counts(1)[1])
#
# print('Minmax_4',Minmax_agent_4_csv.head(0),Minmax_agent_4_csv.shape)
# print(Minmax_agent_4_csv['Winner'].value_counts(1))
# print(Minmax_agent_4_csv['Winner'].value_counts(1)[-1])
# """Win rate"""
# x = ['Minimax_1','Minimax_2','Minimax_3','Minimax_4']
# y = [Minmax_agent_1_csv['Winner'].value_counts(1)[1],Minmax_agent_2_csv['Winner'].value_counts(1)[1],Minmax_agent_3_csv['Winner'].value_counts(1)[1],Minmax_agent_4_csv['Winner'].value_counts(1)[-1]]
# plt.bar(x,y,width=0.3)
# plt.title('Win Rate For Minimax agents(against each other)')
# plt.xlabel('Agent')
# plt.ylabel('Win rate')
# plt.legend()
# plt.minorticks_on()
# plt.grid(alpha=0.5)
# plt.savefig('Win_Rate_For_Minimax_1_2_3_4.png')
# plt.show()
# csv_list = pd.concat(csv_list)
# print(csv_list.head(0))
# print(csv_list.shape)
# print(csv_list.head(1)['Move Time'])
# print(csv_list.iloc[0]['Move Time'])

# """move time"""
# tem = []
# for i in range(0,csv_list.shape[0]):
#     minimax_4 = csv_list.iloc[i]['Move Time']
#     minimax_4_time=json.loads(minimax_4)
#     # print(minimax_4_time[1])
#     if tem == []:
#         tem = minimax_4_time[1]
#     else:
#         tem = [i+j for i,j in zip(tem,minimax_4_time[1])]
# print([i/csv_list.shape[0] for i in tem])
# y = list(range(1,len(tem)+1))
# x = [i/csv_list.shape[0] for i in tem]
# plt.plot(y,x)
# plt.show()

# """move time"""
# Minmax_agent_5_csv = pd.concat(Minmax_agent_5_csv_list)
# minimax_5_time = Minmax_agent_5_csv.iloc[0]['Move Time']
# minimax_5_time = json.loads(minimax_5_time)
# print(minimax_5_time[1])
# print(sum(minimax_5_time[1]))
#
#
# alpha_agent_5_csv = pd.concat(alpha_agent_5_csv_list)
# alpha_agent_5_time = alpha_agent_5_csv.iloc[100]['Move Time']
# alpha_agent_5_time = json.loads(alpha_agent_5_time)
# print(alpha_agent_5_time[1])
# print(sum(alpha_agent_5_time[1]))
#
#
# y = list(range(1, len(minimax_5_time[1]) + 1))
# print(y)
# x = minimax_5_time[1]
# plt.plot(y,x,'co-',label='Minimax_5')
#
# yy = list(range(1, len(alpha_agent_5_time[1]) + 1))
# print(yy)
# xx = alpha_agent_5_time[1]
# plt.plot(yy,xx,'mo-',label='Alpha_beta_5')
#
# plt.title('Move Time For Minimax_5 and Alpha_Beta_5')
# plt.xlabel('Move',)
# plt.ylabel('Move time/s')
# plt.legend()
# plt.minorticks_on()
# plt.grid()
# # plt.savefig('Move_Time_For_Minimax_5.png')
# plt.savefig('Move_Time_For_Minimax_5_and_Alpha_Beta_5.png')
# plt.show()





# print(Eva_csv[0:100]['Winner'].value_counts(1)[1])
#
# name = ['AI(Roxanne)','AI(Random)','AI(Scoremax)','AI(Scoremin)']
# name_eva = ['AI(Random)','AI(Scoremax)','AI(Scoremin)','Total']
# name_ran = ['AI(Roxanne)','AI(Scoremax)','AI(Scoremin)','Total']
# name_scmax = ['AI(Roxanne)','AI(Random)','AI(Scoremin)','Total']
# name_scmin = ['AI(Roxanne)','AI(Random)','AI(Scoremax)','Total']
#
# data_eva = [Eva_csv[0:100]['Winner'].value_counts(1)[1],Eva_csv[100:200]['Winner'].value_counts(1)[1],Eva_csv[200:300]['Winner'].value_counts(1)[1],Eva_csv[0:300]['Winner'].value_counts(1)[1]]
# data_ran = [Ran_csv[0:100]['Winner'].value_counts(1)[1],Ran_csv[100:200]['Winner'].value_counts(1)[1],Ran_csv[200:300]['Winner'].value_counts(1)[1],Ran_csv[0:300]['Winner'].value_counts(1)[1]]
# data_scmax = [Scmax_csv[0:100]['Winner'].value_counts(1)[1],Scmax_csv[100:200]['Winner'].value_counts(1)[1],Scmax_csv[200:300]['Winner'].value_counts(1)[1],Scmax_csv[0:300]['Winner'].value_counts(1)[1]]
# data_scmin = [Scmin_csv[0:100]['Winner'].value_counts(1)[1],Scmin_csv[100:200]['Winner'].value_counts(1)[1],Scmin_csv[200:300]['Winner'].value_counts(1)[1],Scmin_csv[0:300]['Winner'].value_counts(1)[1]]
# data = [data_eva,data_ran,data_scmax,data_scmin]
# figure, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 6),sharey='row')#
# figure.suptitle('Basic Agents Performance', fontsize=20)
# figure.subplots_adjust(wspace=0.1)
# # figure.autofmt_xdate()
#
# ax1.scatter(name_eva,data_eva,marker='o',c=[ 'red','blue','green','black'])
# ax1.set_ylim(0,1)
# ax1.minorticks_on()
# ax1.grid(True,linestyle='-.',color='black',alpha=0.5)
# ax1.set_ylabel('Winning Rate', fontsize=15)
# ax1.set_xlabel('Opposite Agents', fontsize=15)
# ax1.set_title('AI(Roxanne)')
#
# ax2.scatter(name_ran,data_ran,marker='o',c=[ 'red','blue','green','black'])
# # ax2.set_ylim(0,1)
# ax2.grid(True,linestyle='-.',color='black',alpha=0.5)
# ax2.set_title('AI(Random)')
# ax2.set_xlabel('Opposite Agents', fontsize=15)
#
# ax3.scatter(name_scmax,data_scmax,marker='o',c=[ 'red','blue','green','black'])
# ax3.grid(True,linestyle='-.',color='black',alpha=0.5)
# ax3.set_title('AI(Scoremax)')
# ax3.set_xlabel('Opposite Agent', fontsize=15)
#
# ax4.scatter(name_scmin,data_scmin,marker='o',c=[ 'red','blue','green','black'])
# ax4.grid(True,linestyle='-.',color='black',alpha=0.5)
# ax4.set_title('AI(Scoremin)')
# ax4.set_xlabel('Opposite Agents', fontsize=15)
#
# plt.savefig('Basic_Agents_Performance.png')
# plt.show()

# plt.scatter(name[0],data[0][0])
# plt.scatter(name[0],data[0][1])
# plt.scatter(name[0],data[0][2])
# plt.xlabel('Agent',)
# plt.ylabel('Winning Probability')
# plt.ylim(0,1)
# plt.show()
