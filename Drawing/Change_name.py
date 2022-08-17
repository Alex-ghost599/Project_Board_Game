#Liangyz
#2022/8/16  12:46
import os

for root, dirs, files in os.walk("D:\\Durham\\Project\\code\\Data_collection"):
    # print(1,root) #当前目录路径
    # print(2,dirs) #当前路径下所有子目录list
    # print("")
    for dir_name in dirs:
        if "[" and "]" in dir_name:
            old_dir_path=root+"\\"+dir_name
            new_dir_name=dir_name.replace('[','')
            new_dir_name=new_dir_name.replace(']','')
            new_dir_path=root+"\\"+new_dir_name
            print('old_dir_path:',old_dir_path)
            print('new_dir_path:',new_dir_path)
            os.rename(old_dir_path,new_dir_path)

        dir_path=root+"\\"+dir_name

        for root_2, dirs_2, files_2 in os.walk(dir_path):
            for dir_name_2 in dirs_2:
                if "[" and "]" in dir_name_2:
                    old_dir_path_2=root_2+"\\"+dir_name_2
                    new_dir_name_2=dir_name_2.replace('[','')
                    new_dir_name_2=new_dir_name_2.replace(']','')
                    new_dir_path_2=root_2+"\\"+new_dir_name_2
                    print('old_dir_path_2:',old_dir_path_2)
                    print('new_dir_path_2:',new_dir_path_2)
                    os.rename(old_dir_path_2,new_dir_path_2)
            for file_name_2 in files_2:
                if "[" and "]" in file_name_2:
                    old_file_path_2=root_2+"\\"+file_name_2
                    new_file_name_2=file_name_2.replace('[','')
                    new_file_name_2=new_file_name_2.replace(']','')
                    new_file_path_2=root_2+"\\"+new_file_name_2
                    print('old_dir_path_2:',old_file_path_2)
                    print('new_dir_path_2:',new_file_path_2)
                    os.rename(old_file_path_2,new_file_path_2)

