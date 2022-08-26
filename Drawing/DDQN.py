#Liangyz
#2022/8/16  11:51

import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
import os,glob
"""4 agent"""
Alpha_agent = 'AI(Alpha_Beta_4)'
DDQN_agent = 'AI(DQN)'

# DDQN_agent = 'AI(DQN)'
# eva_agent = 'AI(Evaluate)'
# ,Minmax_agent_1
target_agent_list = [Alpha_agent,DDQN_agent]
"""get csv"""
file_path= "D:\\Durham\\Project\\code\\Data_collection"
folder_dir = os.listdir(file_path)
count = 0

Alpha_VS_DQN_csv_list = []


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
                    for csv_name in all_csv_name:
                        Alpha_VS_DQN_csv_list.append(pd.read_csv(csv_name))

Alpha_VS_DQN_csv_df = pd.concat(Alpha_VS_DQN_csv_list)
print(Alpha_VS_DQN_csv_df.head(0),Alpha_VS_DQN_csv_df.shape)
print(Alpha_VS_DQN_csv_df['Winner'].value_counts(1))

"""Win rate"""
# x = ['Alpha_agent','DDQN_agent']
# y = [Alpha_VS_DQN_csv_df['Winner'].value_counts(1)[1],Alpha_VS_DQN_csv_df['Winner'].value_counts(1)[-1]]
#
# plt.bar(x,y,width=0.5,color='darkblue')
# plt.xlabel('Agents')
# plt.ylabel('Wining rate')
# plt.title('Alpha_agent VS. DDQN_agent')
# plt.grid(True,linestyle='-.',alpha=0.3)
# plt.minorticks_on()
# plt.savefig('Alpha_agent_VS._DDQN_agent.png')
# plt.show()
plt.pie(Alpha_VS_DQN_csv_df['Winner'].value_counts(1),
        labels=['Alpha_beta Win','DDQN WIN','Draw'],
        autopct='%1.1f%%',
        shadow=False,
        startangle=270,
        pctdistance=0.6,
        radius=1.1,
        labeldistance=1.05,
        textprops={'fontsize':12},
        explode=[0.05,0.05,0.05],)
plt.title('Score distribution for Alpha_agent VS. DDQN_agent')
plt.savefig('Alpha_agent_VS._DDQN_agent.png')
plt.show()


"""Time"""
time_list_Alpha = []
time_list_DQN = []
for n in (0,1):
    if n == 0:
        print('max time for Alpha_4')
    else:
        print('max time for DQN')
    max_time_l = []
    for i in range(len(Alpha_VS_DQN_csv_df)):
        max_time_list_s = Alpha_VS_DQN_csv_df.iloc[i]['Move Time']
        max_time_list = json.loads(max_time_list_s)
        max_time_l.append(max(max_time_list[n]))
        if n == 0:
            time_list_Alpha.append(max_time_list[n])
        else:
            time_list_DQN.append(max_time_list[n])
    print(max(max_time_l))
print('------------------------------')
move_count_list_Alpha = []
for game in time_list_Alpha:
    move_count_list_Alpha.append(len(game))
print(max(move_count_list_Alpha))
move_count_list_DQN = []
for game in time_list_DQN:
    move_count_list_DQN.append(len(game))
print(max(move_count_list_DQN))
print('------------------------------')
"""Mean move time"""
mean_move_time_list_Alpha = []
for i in range(max(move_count_list_Alpha)):
    move_time = 0
    count = 0
    for game in time_list_Alpha:
        if i<len(game):
            move_time+=game[i]
            count+=1
    mean_move_time_list_Alpha.append(move_time/count)

mean_move_time_list_DQN = []
for i in range(max(move_count_list_DQN)):
    move_time = 0
    count = 0
    for game in time_list_DQN:
        if i<len(game):
            move_time+=game[i]
            count+=1
    mean_move_time_list_DQN.append(move_time/count)

xx = list(range(1,len(mean_move_time_list_Alpha)+1))
yy = mean_move_time_list_Alpha
plt.plot(xx,yy,'bo-',label='Alpha_agent')

xxx = list(range(1,len(mean_move_time_list_DQN)+1))
yyy = mean_move_time_list_DQN
plt.plot(xxx,yyy,'go-',label='DDQN_agent')
plt.legend()
plt.xlabel('Move')
plt.ylabel('Mean move time/s')
plt.title('Mean move time for Alpha_agent and DDQN_agent over 1000 games')
plt.grid(True,linestyle='-.',alpha=0.3)
plt.minorticks_on()
plt.savefig('Mean_move_time_for_Alpha_agent_and_DDQN_agent_over_1000_games.png')
plt.show()
