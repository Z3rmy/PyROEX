# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 17:47:11 2025

@author: 22185
"""
import pandas as pd
import copy
import numpy as np
from function import *
import os
import matplotlib.pyplot as plt
import shutil
from datetime import datetime


class Ion_File():
    def __init__(self):
        self.OCC_time = {'year': [], 'month': [], 'day': [], 'hour': [], 'mintes': [], 'sec': [], 'time': []}
        self.OCC_begin_time ='' ; self.OCC_end_time=''
        
        self.sat='' ; self.sat_number = 0
        self.OCC = {} ; self.dOCC = {} ; self.OCC_MW = {} ; self.OCC_GF = {}; self.OCC_IF = {} ;self.OCC_IOD = {} 
        self.OCC_filter = {} ; self.OCC_DI={}
        self.OCC_str=[]
        self.F_B = -1  ; self.SETTING = -1
        self.OCC_L=[]
        self.OCC_C=[]
        self.OCC_S=[]
        self.lael_kb=''
        self.filero = ''
        self.timetype = ''
        self.OCC_bad_data = {}
        
    def read_file(self,filename):
        '''
        读取头文件
        '''
        self.__init__()
        self.filero = os.path.split(filename)[-1] 
        with open(filename, 'r') as f: 
            for num, read_line in enumerate(f):
                line_lst = read_line.split() 
                line_str= read_line.rstrip()
                
                if line_str[-12:] == 'OCC FOR/BACK':  
                    self.F_B = int(line_lst[0])  
                
                if line_lst[-1] == 'SETTING':  
                    self.SETTING = int(line_lst[0])   
                    #掩星上升或下降
        
                if line_str[-9:] == 'OCC SAT #':
                    self.sat = line_lst[0]
                    self.sat_number = 1
                
                if line_str[-18:] == 'SYS / # /OBS TYPES':
                    length = len(line_lst) - 5  
        
                    for i in range(2, length ):    #从2开始，读取观测量描述符
                    #例如：L2I L5X S2I S5X C2I C5
                        s=line_lst[i]
                        ss={s:[]}
                        self.OCC.update(ss) 
                        self.OCC_DI.update(ss)
                        self.OCC_str.append(s)    
        
                if line_str[-17:] == 'TIME OF FIRST OBS':
                    self.OCC_begin_time = line_lst[0] + '-' + line_lst[1] + '-' + line_lst[2] + ' ' + line_lst[3] + ':' + line_lst[4] + ':' + line_lst[5]
                    self.timetype = line_lst[-5]
                if line_str[-16:] == 'TIME OF LAST OBS':
                    self.OCC_end_time = line_lst[0] + '-' + line_lst[1] + '-' + line_lst[2] + ' ' + line_lst[3] + ':' + line_lst[4] + ':' + line_lst[5]
        
                if line_str[-13:]=='END OF HEADER':
                    self.line_of_head = num
        
        with open(filename, 'r') as f: 
            read_all = f.readlines() 
            for read_line in read_all[self.line_of_head+1 :]:
                line_lst = read_line.split() 
                line_str= read_line.rstrip()
                
                if line_str[0] == r'>':
                    self.OCC_time['year'].append(float(line_lst[1]))
                    self.OCC_time['month'].append(float(line_lst[2]))
                    self.OCC_time['day'].append(float(line_lst[3]))
                    self.OCC_time['hour'].append(float(line_lst[4]))
                    self.OCC_time['mintes'].append(float(line_lst[5]))
                    self.OCC_time['sec'].append(float(line_lst[6]))
                    self.OCC_time['time'].append(str('%4d' % int(line_lst[1])) + '-' + str('%02d' % int(line_lst[2])) + '-' + str(
                        '%02d' % int(line_lst[3])) + ' ' + str('%02d' % int(line_lst[4])) + ':' + str(
                        '%02d' % int(line_lst[5])) + ':' + str('%2.2f' % float(line_lst[6][0:5])))
                            
                elif line_lst[0] == self.sat:
        
                    for i in range(len(self.OCC_str)):
                        self.OCC[self.OCC_str[i]].append(float(line_lst[i+1]))
                    
                else:
                    continue
        
        '''
        ==================
        文件数据读取完毕
        ==================
        '''
        if len(self.OCC_time['time']) > 0:
            self.OCC_time_list = pd.DatetimeIndex(self.OCC_time['time'])

            self.OCC_dif = np.diff(self.OCC_time_list ).astype(float)/1000000000
            #np.diff 会返回一个数组(array)，表示相邻时间戳之间的时间差，单位为纳秒。  /1e9
        
        
        if self.SETTING == 0:
            self.label_kb = 'RISING'
        if self.SETTING == 1:
            self.label_kb = 'SETTING'
            

        
        for i in range(len(self.OCC_str)):
            s=self.OCC_str[i] 
            if s[0] == 'L':
                self.OCC_L.append(s)
            elif s[0] == 'S':
                self.OCC_S.append(s)
            elif s[0] == 'C':
                self.OCC_C.append(s)
        

         
         
        self.OCC_time_length = len(self.OCC_time_list)  

                # plt.plot(self.OCC_MP[LLC1],'.',label=LLC1)
            # 

    def SNR_filter(self,SNR_lim=40,SNR_LANK=0 ,window_OCC=60):
        self.OCC_filter = copy.deepcopy(self.OCC)
        index_OCC = []
        for tag in self.OCC_S:
            SNR = tag
            # print(SNR)
            '''
            找到SNR_AVE小于等于界限的索引
            '''

            # windows_OCC = 60
            average = vector_moving_average(self.OCC[SNR] , window_OCC)
            
            index_ = find_first_less_or_equal(average , SNR_lim)

            if index_ == 0 :
                
                #如果index_=0并且列表还不为空的话：两种情况
                #一是截取时间过短，可以用file_edit
                #二是接收的数据有问题，中间有部分变化值
                L = "L"+SNR[1:]
                C = "C"+SNR[1:]
                self.OCC_filter[SNR] = np.array(self.OCC_filter[SNR], dtype=np.float64)
                self.OCC_filter[L] = np.array(self.OCC_filter[L], dtype=np.float64)
                self.OCC_filter[C] = np.array(self.OCC_filter[C], dtype=np.float64)
                self.OCC_filter[SNR][:] = np.nan
                self.OCC_filter[L][:] = np.nan
                self.OCC_filter[C][:] = np.nan
                continue
            index_OCC.append(index_)
            
        index_min = min(index_OCC)

        for tag in self.OCC_filter:

            self.OCC_filter[tag] = np.array(self.OCC_filter[tag], dtype=np.float64)
            self.OCC_filter[tag][index_min:] = np.nan
        
        if index_min == len(self.OCC_time_list):
            self.filter_OCC_end_time = self.OCC_time_list[-1]
        else:
            self.filter_OCC_end_time = self.OCC_time_list[index_min]
            
        '''
        变化率
        '''
        for i in range(len(self.OCC_str)):
            s=self.OCC_str[i]
            self.dOCC[s]= np.diff(self.OCC_filter[s])/self.OCC_dif
            
        for i in range(len(self.OCC_L)):
            si = self.OCC_L[i]
            fi = find_frequence(si[1:],self.sat)
            Pi = np.array(self.OCC_filter[si]) ; Ci = np.array(self.OCC_filter['C'+si[1:]])

            for  j in range(i+1,len(self.OCC_L)):
                sj = self.OCC_L[j]
                fj = find_frequence(sj[1:],self.sat)
                Pj = np.array(self.OCC_filter[sj]) ; Cj = np.array(self.OCC_filter['C'+sj[1:]])
                LL = si[1:]+sj[1:] ; LLC1 = si[1:]+sj[1:] + si[1:] ; LLC2 = si[1:]+sj[1:] + sj[1:]
                
                
                self.OCC_MW.update({LL:[]})  ; self.OCC_MW[LL] = MW_COMB(Pi,Pj,Ci,Cj,fi,fj)
                self.OCC_GF.update({LL:[]})  ; self.OCC_GF[LL] = GF_COMB_2(Pi, Pj, fi, fj)
                self.OCC_IF.update({LL:[]}); self.OCC_IF[LL] = IF_COMB(Pi, Pj, fi, fj)
        
               

    def DI_CHECK(self):

        OCC_time_full = pd.date_range(
        start=self.OCC_begin_time,
        end=str(self.filter_OCC_end_time),
        freq='1s'  
        )

        self.missing_time_OCC = OCC_time_full.difference(self.OCC_time_list)
        for tag in self.OCC_DI:
            self.OCC_DI[tag] = 1-len(self.missing_time_OCC)/len(OCC_time_full)

        self.OCC_bad_data ={}
        
        for i in range(len(self.missing_time_OCC)):
            time_tag = self.missing_time_OCC[i]
            self.OCC_bad_data[time_tag] = self.OCC_str
        # print(self.data_integrity_OCC)
    def write_DI(self):
        '''
        将信息写入LOG文件
        包括：
        检测文件
        文件类型
        数据完整度，1个
        TIME 
        卫星标记   缺失数据标识   
        '''
        current_dir = os.getcwd()

        # 定义 LOG 文件夹路径
        parent_dir = os.path.dirname(current_dir)
        # 定义上一层目录中的 data/LOG 路径
        log_dir = os.path.join(parent_dir, 'data', 'LOG')
        
        # 如果 LOG 文件夹不存在，则创建它
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 构建文件路径
        file_to_write = os.path.join(log_dir, 'LOG_DI_' + self.filero)

        file_to_write = file_to_write[:-4] + '.txt'
        self.log_DI = file_to_write
        
        
        with open(file_to_write, 'w') as file:
            file.write(self.filero + '\n')
            file.write('file type: I\n')
            file.write('\n')
            file.write(f'{self.sat}_DATA_INTEGRETY\n')
            for tag in self.OCC_DI:
                
                file.write(f'{tag}: {self.OCC_DI[tag] * 100:.2f}% \n\n')
            # 格式化其他数据
            file.write('\n')
            if not self.missing_time_OCC.empty:
                for time_tag in self.missing_time_OCC:

                    file.write(f'TIME {time_tag} \n')
                    file.write(f'{self.sat}  {self.OCC_bad_data[time_tag]} \n')
                
            # Show_file(file_to_write)
        return file_to_write
    
    def Edit_Ion(self,input_filename,start_time,end_time,output_filename):
        if output_filename[-4:]!='.ROX':
            output_filename = output_filename+'.ROX'
        s_time = pd.Timestamp(start_time)
        e_time = pd.Timestamp(end_time)
        
        # print(s_time,e_time)
            
        in_s_time = s_time in self.OCC_time_list
        in_e_time = e_time in self.OCC_time_list
        
        all_sec   = (self.OCC_time_list[-1] - self.OCC_time_list[0]).total_seconds()

        
        warning = ''
        '''
        异常处理
        得到 warning信息，然后在app内以警告框形式呈现
        '''
        if not in_s_time:
           warning = 'Ion start time entered is not within the valid time range'
           return False,warning   
          
        if not in_e_time:
           warning = 'Ion end time entered is not within the valid time range'
           return False,warning
            
       
        if not is_valid_datetime(start_time):
           warning = 'ION start time does not meet the required time format'  
           return False,warning
        if not is_valid_datetime(end_time):
           warning = 'ION end time does not meet the required time format'
           return False,warning
        
        '''
        异常处理
        '''
        gap_time = (e_time - s_time).total_seconds()

        
        shutil.copy(input_filename,output_filename)
        with open(output_filename, 'r') as f: 
            lines = f.readlines()
        
        processed_lines = []
        start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
        end_datetime   = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
        
        for read_line in lines[:self.line_of_head + 1]:
            line_str= read_line.rstrip()
            if line_str[-17:] == 'TIME OF FIRST OBS':
                microsecond = start_datetime.microsecond * 10  
    
                # 格式化秒和微秒，确保微秒是7位
                formatted_second = f"{start_datetime.second:02d}.{microsecond:07d}"
                new_line = f"  {start_datetime.year:4d}    {start_datetime.month:2d}    {start_datetime.day:2d}    {start_datetime.hour:02d}    {start_datetime.minute:02d}   {formatted_second}     GPS         TIME OF FIRST OBS\n"
                processed_lines.append(new_line)
            elif line_str[-16:] == 'TIME OF LAST OBS':
                microsecond = end_datetime.microsecond * 10 
                # 格式化秒和微秒，确保微秒是7位
                formatted_second = f"{end_datetime.second:2d}.{microsecond:07d}"
                new_line = f"  {end_datetime.year:4d}    {end_datetime.month:2d}    {end_datetime.day:2d}    {end_datetime.hour:02d}    {end_datetime.minute:02d}   {formatted_second}     GPS         TIME OF LAST OBS\n"
                processed_lines.append(new_line)
                
            else:
                processed_lines.append(read_line)
        
        
        for index ,read_line in enumerate(lines):
            '''
            找到时间戳对应
            '''
            line_str= read_line.rstrip()
            if line_str[0] == r'>':
                timestamp_str = read_line[1:].strip().split()[0:6]
                
                ts_str = f"{timestamp_str[0]} {timestamp_str[1]} {timestamp_str[2]} {timestamp_str[3]} {timestamp_str[4]} {timestamp_str[5][:-1]}"
                #%.f表示微妙范围为 0 - 999999，但是atm文件中给了七位小数
                   # 转换为 datetime 对象       
                current_datetime = datetime.strptime(ts_str, "%Y %m %d %H %M %S.%f")
                if start_datetime == current_datetime:
                    start_OCC = index 
                    # print(index)
                if end_datetime == current_datetime:
                    end_OCC = index  

        for index in range(start_OCC , end_OCC+2 , 2):
            processed_lines.append(lines[index])
            processed_lines.append(lines[index+1])
            
       # 获取当前目录
        current_dir = os.getcwd()
    # 上一级目录
        parent_dir = os.path.dirname(current_dir)
    # 上一级目录中的data文件夹路径
        data_dir = os.path.join(parent_dir, "data")
    
    # 确保data文件夹存在（不存在则创建）
        os.makedirs(data_dir, exist_ok=True)
    
    # 完整的输出文件路径（上一级/data/文件名）
        full_output_path = os.path.join(data_dir, output_filename)

    
        with open(full_output_path, 'w', encoding='utf-8') as target_file:
           for content in processed_lines:  # processed_lines是你的内容列表
             target_file.write(content)
        print(full_output_path)
        return True , warning
    
if __name__ == "__main__":   
    filename=r"C:\Users\zhangmingyi24\OneDrive\Desktop\ROEX分析软件开源程序论文\ROEX分析软件开源程序论文\ROEX分析软件代码\PyROEX_论文\data\occIon_GNOS.007.G02.2024.052.05760.0644.00.0000_bin.ROX"
    # filename=r"C:\Users\zhangmingyi24\OneDrive\Desktop\ROEX分析软件开源程序论文\ROEX分析软件开源程序论文\ROEX分析软件代码\PyROEX\data\processed_ion.ROX"
    # filename = r"C:\Users\zhangmingyi24\OneDrive\Desktop\ROEX分析软件开源程序论文\ROEX分析软件开源程序论文\ROEX分析软件代码\PyROEX\data\processed_ion - 副本.ROX"
    filename = r"C:\Users\zhangmingyi24\OneDrive\Desktop\ROEX分析软件开源程序论文\ionRox_GPS_2024.152\ionRox_GPS_2024.152\occIon_GNOS.007.G15.2024.152.02064.0661.00.0000_bin.ROX"
    test =Ion_File()
    test.read_file(filename)
    test.SNR_filter(0,0)
    # test.DI_CHECK()
    # test.write_DI()
    outfile_name = "processed_ion"
    jug,warning = test.Edit_Ion(filename, "2024-2-21 1:37:30.00", "2024-2-21 1:46:43.00", outfile_name)
    # Show_file("IonIon.ROX")