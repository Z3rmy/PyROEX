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
        self.OCC_filter = {}
        self.OCC_str=[]
        self.F_B = -1  ; self.SETTING = -1
        self.OCC_L=[]
        self.OCC_C=[]
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
                        '%02d' % int(line_lst[3])) + '\n' + str('%02d' % int(line_lst[4])) + ':' + str(
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
            #CLO_time['time'] 是一个字符串列表，其中包含格式为 'YYYY-MM-DD HH:MM:SS.SS' 的时间戳
            self.OCC_dif = np.diff(self.OCC_time_list ).astype(float)/1000000000
            #np.diff 会返回一个数组(array)，表示相邻时间戳之间的时间差，单位为纳秒。  /1e9
        
        
        if self.SETTING == 0:
            self.label_kb = 'UP'
        if self.SETTING == 1:
            self.label_kb = 'DOWN'
            

        
        for i in range(len(self.OCC_str)):
            s=self.OCC_str[i] 
            if s[0] == 'L':
                self.OCC_L.append(s)

        
        for i in range(len(self.OCC_str)):
            s=self.OCC_str[i]
            if s[0] == 'C':
                self.OCC_C.append(s)
         
         
        self.OCC_time_length = len(self.OCC_time_list)  

                # plt.plot(self.OCC_MP[LLC1],'.',label=LLC1)
            # 
                
        '''
        ================================
        过滤数据，保留信噪比大于等于40的数据
        只需过滤OCC数据即可
        '''

    def SNR_filter(self,SNR_lim=40,SNR_BLANK=0):
        self.OCC_filter = copy.deepcopy(self.OCC)

        '''
        时间差分
        '''
        for i in range(len(self.OCC_str)):
            s=self.OCC_str[i]
            self.dOCC[s]= np.diff(self.OCC[s])/self.OCC_dif
        # SNR_lim = 40
        
        for time in range(len(self.OCC_time_list)):
            for tag in self.OCC_filter:
                SNR = 'S'+ tag[1:]
            
                if self.OCC_filter[SNR][time] < SNR_lim or np.isnan(self.OCC_filter[SNR][time]):
                    self.OCC_filter[tag][time] = np.nan
                    if time != len(self.OCC_time_list)-1:
                        self.dOCC[tag][time] = np.nan
        # print(tag)       

        
        for i in range(len(self.OCC_L)):
            si = self.OCC_L[i]
            fi = find_frequence(si[1:],self.sat)
            Pi = np.array(self.OCC[si]) ; Ci = np.array(self.OCC['C'+si[1:]])

            for  j in range(i+1,len(self.OCC_L)):
                sj = self.OCC_L[j]
                fj = find_frequence(sj[1:],self.sat)
                Pj = np.array(self.OCC[sj]) ; Cj = np.array(self.OCC['C'+sj[1:]])
                LL = si[1:]+sj[1:] ; LLC1 = si[1:]+sj[1:] + si[1:] ; LLC2 = si[1:]+sj[1:] + sj[1:]
                
                
                self.OCC_MW.update({LL:[]})  ; self.OCC_MW[LL] = MW_COMB(Pi,Pj,Ci,Cj,fi,fj)
                self.OCC_GF.update({LL:[]})  ; self.OCC_GF[LL] = GF_COMB_2(Pi, Pj, fi, fj)
                self.OCC_IF.update({LL:[]}); self.OCC_IF[LL] = IF_COMB(Pi, Pj, fi, fj)
          
                
        for time in range(len(self.OCC_time_list)-1):
            for i in range(len(self.OCC_L)):
                si = self.OCC_L[i]
                Si = 'S' + si[1:]
                for  j in range(i+1,len(self.OCC_L)):
                    sj = self.OCC_L[j]
                    Sj = 'S'+sj[1:]
                    LL = si[1:]+sj[1:] 
                    if np.isnan(self.OCC_filter[Si][time]) or np.isnan(self.OCC_filter[Sj][time]):
                        self.OCC_MW[LL][time] = np.nan
                        self.OCC_GF[LL][time] = np.nan
                        self.OCC_IF[LL][time] = np.nan
               

    def DI_CHECK(self):
        non_nan_count_OCC = np.sum(~np.isnan(self.OCC_filter['S'+self.OCC_L[0][1:]]))
        self.ideal_data_OCC  = len(self.OCC_str) *non_nan_count_OCC   
        self.actual_data_OCC = self.ideal_data_OCC

        for i in range(len(self.OCC_time_list)):
            time_tag = self.OCC_time_list[i]
            self.OCC_bad_data[time_tag] = []

            for s in self.OCC_str:
                if self.OCC_filter[s][i] == 0:
                    self.OCC_bad_data[time_tag].append(s)
                    self.actual_data_OCC -= 1
        

        self.data_integrity_OCC = self.actual_data_OCC / self.ideal_data_OCC 
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
        log_dir = os.path.join(current_dir, 'LOG')
        
        # 如果 LOG 文件夹不存在，则创建它
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 构建文件路径
        file_to_write = os.path.join(log_dir, 'LOG_DI_' + self.filero)

        file_to_write = file_to_write[:-4] + '.txt'
        self.log_DI = file_to_write
        
        
        with open(file_to_write, 'w') as file:
            file.write(self.filero + '\n'+'\n')
            file.write('file type: A\n')
            file.write(f'DATA_INTEGRETY_OCC: {self.data_integrity_OCC * 100:.2f}% \n\n')
            # 格式化其他数据
            for i in range(self.OCC_time_length):
                time_tag = self.OCC_time_list[i]
                if  self.OCC_bad_data[time_tag]: 
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
                new_line = f"  {start_datetime.year:4d}    {start_datetime.month:2d}    {start_datetime.day:2d}    {start_datetime.hour:02d}    {start_datetime.minute:02d}   {formatted_second}     GPS         TIME OF FIRST CLO\n"
                processed_lines.append(new_line)
            elif line_str[-16:] == 'TIME OF LAST OBS':
                microsecond = end_datetime.microsecond * 10 
                # 格式化秒和微秒，确保微秒是7位
                formatted_second = f"{end_datetime.second:2d}.{microsecond:07d}"
                new_line = f"  {end_datetime.year:4d}    {end_datetime.month:2d}    {end_datetime.day:2d}    {end_datetime.hour:02d}    {end_datetime.minute:02d}   {formatted_second}     GPS         TIME OF FIRST CLO\n"
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

        for index in range(start_OCC , end_OCC+3 , 2):
            processed_lines.append(lines[index])
            processed_lines.append(lines[index+1])
            
        with open(output_filename, 'w', encoding='utf-8') as target_file:
            for content in processed_lines:
                target_file.write(content)
            
        return True , warning
    
if __name__ == "__main__":   
    # filename=r"C:\Users\22185\Desktop\GNSS\ROEX分析软件开源程序论文\ionRox\occIon_GNOS.007.C10.2024.052.67370.0567.00.0000_bin.ROX"
    filename=r"C:\Users\22185\Desktop\GNSS\ROEX分析软件开源程序论文\ROEX分析软件开源程序论文\ROEX分析软件代码\ROEX_analysis_2\occIon_GNOS.007.C10.2024.052.67370.0567.00.0000_bin.ROX"
    test =Ion_File()
    test.read_file(filename)
    test.SNR_filter()
    test.DI_CHECK()
    test.write_DI()
    # jug,warning = test.Edit_Ion(filename, "2024-2-21 18:42:56.00", "2024-2-21 18:43:56.00", "IonIon")
    # Show_file("IonIon.ROX")