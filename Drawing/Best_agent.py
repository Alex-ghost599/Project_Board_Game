#Liangyz
#2022/8/16  11:51

import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
import os,glob
"""4 agent"""
Minimax_agent_ = 'AI(MinMax_4)'
Alpha_agent = 'AI(Alpha_Beta_4)'
Mcts_agent = 'AI(MCTS_200)'
# DDQN_agent = 'AI(DQN)'
# eva_agent = 'AI(Evaluate)'
# ,Minmax_agent_1
target_agent_list = [Minimax_agent_,Alpha_agent,Mcts_agent]
"""get csv"""
file_path= "D:\\Durham\\Project\\code\\Data_collection"
folder_dir = os.listdir(file_path)
count = 0
Minimax_VS_Alpha_list = []
Minimax_VS_Mcts_list = []
Alpha_VS_Mcts_list = []


for folder in folder_dir:
    if folder in target_agent_list:
        file_dir = os.listdir(file_path + "\\" + folder)
        for file in file_dir:
            if file in target_agent_list:
            # if file is Minmax_agent_4:
                csv_path = file_path + "\\" + folder + "\\" + file + "\\" + folder + "_VS_"+ file
                # print(csv_path)
                # target_csv_path = csv_path + "\\" + folder + "_VS_" + file + "_2022-08-1" + "*.csv"+ "_2022-08-1"
                target_csv_path = csv_path + "\\" + folder + "_VS_" + file + "*.csv"

                # print(target_csv_path)
                all_csv_name = glob.glob(target_csv_path)
                # all_csv_name_4 = glob.glob(target_csv_path_4)
                # all_csv_name_5 = glob.glob(target_csv_path_5)
                # all_csv_name_ab_5 = glob.glob(target_csv_path_ab_5)
                print(all_csv_name)
                print('------------------------------')
                if all_csv_name != []:
                    if folder == Minimax_agent_ and file == Alpha_agent:
                        for csv_name in all_csv_name:
                            Minimax_VS_Alpha_list.append(pd.read_csv(csv_name))
                    elif folder == Minimax_agent_ and file == Mcts_agent:
                        for csv_name in all_csv_name:
                            Minimax_VS_Mcts_list.append(pd.read_csv(csv_name))
                    elif folder == Alpha_agent and file == Mcts_agent:
                        for csv_name in all_csv_name:
                            Alpha_VS_Mcts_list.append(pd.read_csv(csv_name))

Minimax_VS_Alpha_df = pd.concat(Minimax_VS_Alpha_list)
Minimax_VS_Mcts_df = pd.concat(Minimax_VS_Mcts_list)
Alpha_VS_Mcts_df = pd.concat(Alpha_VS_Mcts_list)

print('Minimax_4_vs_Alpha_4')
print(Minimax_VS_Alpha_df.head(0),Minimax_VS_Alpha_df.shape)
print(Minimax_VS_Alpha_df['Winner'].value_counts(1))
print('------------------------------')
print('Minimax_4_vs_Mcts_200')
print(Minimax_VS_Mcts_df.head(0),Minimax_VS_Mcts_df.shape)
print(Minimax_VS_Mcts_df['Winner'].value_counts(1))
print('------------------------------')
print('Alpha_4_vs_Mcts_200')
print(Alpha_VS_Mcts_df.head(0),Alpha_VS_Mcts_df.shape)
print(Alpha_VS_Mcts_df['Winner'].value_counts(1))

print('------------------------------')
print("Time")
time_list_Minimax = []
time_list_Alpha = []
time_list_Mcts = []
for n in (0,1):
    if n == 0:
        print('max time for Minimax_4')
    else:
        print('max time for Alpha_4')
    max_time_l = []
    for i in range(len(Minimax_VS_Alpha_df)):
        max_time_list_s = Minimax_VS_Alpha_df.iloc[i]['Move Time']
        max_time_list = json.loads(max_time_list_s)
        max_time_l.append(max(max_time_list[n]))
        if n == 0:
            time_list_Minimax.append(max_time_list[n])
        else:
            time_list_Alpha.append(max_time_list[n])
    print(max(max_time_l))
print('-------------')
for n in (0,1):
    if n == 0:
        print('max time for Minimax_4')
    else:
        print('max time for Mcts_200')
    max_time_l = []
    for i in range(len(Minimax_VS_Mcts_df)):
        max_time_list_s = Minimax_VS_Mcts_df.iloc[i]['Move Time']
        max_time_list = json.loads(max_time_list_s)
        max_time_l.append(max(max_time_list[n]))
        if n == 0:
            time_list_Minimax.append(max_time_list[n])
        else:
            time_list_Mcts.append(max_time_list[n])
    print(max(max_time_l),max_time_l.index(max(max_time_l)))
    # print(Minimax_VS_Mcts_df.iloc[max_time_l.index(min(max_time_l))]['Move Time'])
print('-------------')
for n in (0,1):
    if n == 0:
        print('max time for Alpha_4')
    else:
        print('max time for Mcts_200')
    max_time_l = []
    for i in range(len(Alpha_VS_Mcts_df)):
        max_time_list_s = Alpha_VS_Mcts_df.iloc[i]['Move Time']
        max_time_list = json.loads(max_time_list_s)
        max_time_l.append(max(max_time_list[n]))
        if n == 0:
            time_list_Alpha.append(max_time_list[n])
        else:
            time_list_Mcts.append(max_time_list[n])
    print(max(max_time_l))

"""Win rate"""
# y1_Minimax =[Minimax_VS_Alpha_df['Winner'].value_counts(1)[1],Minimax_VS_Mcts_df['Winner'].value_counts(1)[1]]
# y2_Alpha =[Minimax_VS_Alpha_df['Winner'].value_counts(1)[-1],Alpha_VS_Mcts_df['Winner'].value_counts(1)[1]]
# y3_Mcts =[Minimax_VS_Mcts_df['Winner'].value_counts(1)[-1],Alpha_VS_Mcts_df['Winner'].value_counts(1)[-1]]
#
# x1 = ['Alpha_4','Mcts_200']
# x2 = ['Minimax_4','Mcts_200']
# x3 = ['Minimax_4','Alpha_4']
#
# plt.bar(x1,y1_Minimax,label='Minimax_4',width=0.5)
# plt.ylim(0,1)
# plt.legend(loc=2)
# plt.title('Minimax 4')
# plt.ylabel('Winning Rate')
# plt.xlabel('Opposite Agent')
# plt.grid(True,linestyle='-.',alpha=0.3)
# plt.minorticks_on()
# plt.text('Alpha_4',Minimax_VS_Alpha_df['Winner'].value_counts(1)[1],str(round(Minimax_VS_Alpha_df['Winner'].value_counts(1)[1],3))+'\n',ha='center',va='center',fontsize=12)
# plt.text('Mcts_200',Minimax_VS_Mcts_df['Winner'].value_counts(1)[1],str(round(Minimax_VS_Mcts_df['Winner'].value_counts(1)[1],3))+'\n',ha='center',va='center',fontsize=12)
# plt.savefig('Minimax_4_fin.png')
# plt.show()
#
# plt.bar(x2,y2_Alpha,label='Alpha_4',width=0.5,color='y')
# plt.ylim(0,1)
# plt.legend(loc=2)
# plt.title('Alpha 4')
# plt.ylabel('Winning Rate')
# plt.xlabel('Opposite Agent')
# plt.grid(True,linestyle='-.',alpha=0.3)
# plt.minorticks_on()
# plt.text('Minimax_4',Minimax_VS_Alpha_df['Winner'].value_counts(1)[-1],str(round(Minimax_VS_Alpha_df['Winner'].value_counts(1)[-1],3))+'\n',ha='center',va='center',fontsize=12)
# plt.text('Mcts_200',Alpha_VS_Mcts_df['Winner'].value_counts(1)[1],str(round(Alpha_VS_Mcts_df['Winner'].value_counts(1)[1],3))+'\n',ha='center',va='center',fontsize=12)
# plt.savefig('Alpha_4_fin.png')
# plt.show()
#
# plt.bar(x3,y3_Mcts,label='Mcts_200',width=0.5,color='g')
# plt.ylim(0,1)
# plt.legend(loc=2)
# plt.title('Mcts 200')
# plt.ylabel('Winning Rate')
# plt.xlabel('Opposite Agent')
# plt.grid(True,linestyle='-.',alpha=0.3)
# plt.minorticks_on()
# plt.text('Minimax_4',Minimax_VS_Mcts_df['Winner'].value_counts(1)[-1],str(round(Minimax_VS_Mcts_df['Winner'].value_counts(1)[-1],3))+'\n',ha='center',va='center',fontsize=12)
# plt.text('Alpha_4',Alpha_VS_Mcts_df['Winner'].value_counts(1)[-1],str(round(Alpha_VS_Mcts_df['Winner'].value_counts(1)[-1],3))+'\n',ha='center',va='center',fontsize=12)
# plt.savefig('Mcts_200_fin.png')
# plt.show()

print('-------------')
"""time"""

print(len(time_list_Minimax))
move_count_list_Minimax = []
for game in time_list_Minimax:
    move_count_list_Minimax.append(len(game))
move_count_list_Alpha = []
for game in time_list_Alpha:
    move_count_list_Alpha.append(len(game))
move_count_list_Mcts = []
for game in time_list_Mcts:
    move_count_list_Mcts.append(len(game))
"""mean move time"""
mean_move_time_Minimax = []
for i in range(max(move_count_list_Minimax)):
    move_time = 0
    count = 0
    for game in time_list_Minimax:
        if i < len(game):
            move_time += game[i]
            count += 1
    mean_move_time_Minimax.append(move_time/count)
# print(mean_move_time_Minimax)
mean_move_time_Alpha = []
for i in range(max(move_count_list_Alpha)):
    move_time = 0
    count = 0
    for game in time_list_Alpha:
        if i < len(game):
            move_time += game[i]
            count += 1
    mean_move_time_Alpha.append(move_time/count)
# print(mean_move_time_Alpha)
mean_move_time_Mcts = []
for i in range(max(move_count_list_Mcts)):
    move_time = 0
    count = 0
    for game in time_list_Mcts:
        if i < len(game):
            move_time += game[i]
            count += 1
    mean_move_time_Mcts.append(move_time/count)
# print(mean_move_time_Mcts)



x = list(range(1, max(move_count_list_Minimax) + 1))
y = mean_move_time_Minimax
plt.plot(x,y,'co-',label='Minimax_4')

xx = list(range(1, max(move_count_list_Alpha) + 1))
yy = mean_move_time_Alpha
plt.plot(xx,yy,'yo-',label='Alpha_4')

xxx = list(range(1, max(move_count_list_Mcts) + 1))
yyy = mean_move_time_Mcts
plt.plot(xxx,yyy,'go-',label='Mcts_200')


plt.title('Mean move Time For Minimax, Alpha_Beta and Mcts over 1000 games')
plt.xlabel('Move',)
plt.ylabel('Move time/s')
plt.legend()
plt.minorticks_on()
plt.grid(True,linestyle='-.',alpha=0.5)
plt.savefig('mean_move_time.png')
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
