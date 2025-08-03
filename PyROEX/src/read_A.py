# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 10:04:01 2025

@author: 22185
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
from function import *
import os
import shutil
from datetime import datetime
plt.rcParams['font.sans-serif'] = ['SimHei']    #方便显示中文
plt.rcParams['axes.unicode_minus'] = False

'''
Filter用来画图
原数据用于DI判断
'''
class Atm_File:    
    # filename=''
    
    # filename=r'C:/Users/22185/Desktop/GNSS/ROEX分析软件开源程序论文/atmRox/cloAtm_GNOS.007.G02.06.2024.152.43920.0091.03.0000_bin.ROX'
    # filename = r'C:\Users\22185\Desktop\GNSS\ROEX分析软件开源程序论文\atmRox\cloAtm_GNOS.007.C10.09.2024.152.19615.0102.03.0000_bin.ROX'
    
    # filename = r"C:\Users\22185\Desktop\GNSS\ROEX分析软件开源程序论文\atmRox\cloAtm_GNOS.007.G02.06.2024.152.38667.0115.03.0000_bin.ROX"
    '''
    =================================
    =================================
    读取大气层掩星文件
    =================================
    =================================
    '''
    # def read_and_plot_atm(filename):
    # filero = filename.split('\\')[-1]
    def __init__(self):
        self.filero = ''
        self.CLO_time = {'year': [], 'month': [], 'day': [], 'hour': [], 'mintes': [], 'sec': [], 'time': []}
        self.OPE_time = {'year': [], 'month': [], 'day': [], 'hour': [], 'mintes': [], 'sec': [], 'time': []}
        
        self.OCC_CLO = {}  ; self.dOCC_CLO = {}  ; self.OCC_CLO_MW = {} ; self.OCC_CLO_GF = {}; self.OCC_CLO_IF = {} ; self.OCC_CLO_DIF = {} 
        self.REF_CLO = {}  ; self.dREF_CLO = {}  ; self.REF_CLO_MW = {} ; self.REF_CLO_GF = {}; self.REF_CLO_IF = {} ; 
        self.OCC_OPE = {}  ; self.dOCC_OPE = {}  ; self.OCC_OPE_MW = {} ; self.OCC_OPE_GF = {}; self.OCC_OPE_IF = {} ; self.OCC_OPE_DIF = {} 
        self.REF_OPE = {}  ; self.dREF_OPE = {}  ; self.REF_OPE_MW = {} ; self.REF_OPE_GF = {}; self.REF_OPE_IF = {} ; 
        #数据类型名称
        self.OCC_CLO_filter = {} ; self.OCC_CLO_DI={} ; self.REF_CLO_DI={}
        self.OCC_OPE_filter = {} ; self.OCC_OPE_DI={} ; self.REF_OPE_DI={}
        
        self.OCC_CLO_str = []
        self.REF_CLO_str = []
        self.OCC_OPE_str = []
        self.REF_OPE_str = []
        
        self.sat_number = 0
        self.line_number = 0
        self.SETTING = -1; self.sat1='' ; self.sat2=''
        self.line_of_CLO_start = -1 ; self.line_of_CLO_en = 0; self.line_of_OPE_start=-1; self.line_of_OPE_end =0
        self.label_kb='' ; self.CLO_time_list=[] ; self.OPE_time_list=[]
        self.CLO_time_length = 0
        self.OPE_time_length = 0
        self.timetype = ''
        
        # self.OPE_dif =0.01 ; self.CLO_dif = 0.02;
        
        self.OCC_CLO_L=[]
        self.OCC_OPE_L=[]
        self.OCC_CLO_S=[]
        self.OCC_OPE_S=[]
        self.REF_CLO_L=[]
        self.REF_OPE_L=[]
        
        self.OCC_CLO_C=[]
        self.OCC_OPE_C=[]
        self.REF_CLO_C=[]
        self.REF_OPE_C=[]
        
        self.OCC_OPE_O=[]
        self.OCC_OPE_I=[]
        self.OCC_OPE_Q=[]
        


    '''
    ==================
    读取头文件内容
    ==================
    '''
    def read_file(self , filename):
        self.__init__()
        self.filero = os.path.split(filename)[-1]   #file 字符串按 '/' 分割成一个列表

        with open(filename, 'r') as f: 
            for num, read_line in enumerate(f):
                line_lst = read_line.split() 
                line_str= read_line.rstrip()
                if line_lst[-1] == 'SETTING':  
                    self.SETTING = int(line_lst[0])   
                    #掩星上升或下降
                if line_str[-15:] == 'OCC / REF SAT #':  #两个卫星  
                    self.sat1 = line_lst[0]
                    self.sat2 = line_lst[1]
                    self.sat_number = 2
                if line_str[-9:] == 'OCC SAT #':
                    self.sat1 = line_lst[0]
                    self.sat_number = 1
                
                if line_str[-19:] == 'SYS/#/OCC CLO TYPES':
                    length = len(line_lst) - 3  
                    for i in range(2, length ):    #从2开始，读取观测量描述符
                    #例如：L2I L5X S2I S5X C2I C5
                        s=line_lst[i]
                        ss={s:[]}
                        self.OCC_CLO.update(ss) ; self.dOCC_CLO.update(ss) 
                        self.OCC_CLO_str.append(s)  ;self.OCC_CLO_DI.update(ss)  
                if line_str[-19:] == 'SYS/#/OCC OPE TYPES':
                    length = len(line_lst) - 3
                    for i in range(2, length ):
                        s = line_lst[i]
                        ss = {s: []}
                        self.OCC_OPE.update(ss) ; self.dOCC_OPE.update(ss)
                        self.OCC_OPE_str.append(s) ; self.OCC_OPE_DI.update(ss)
                if line_str[-19:] == 'SYS/#/REF CLO TYPES':
                    length = len(line_lst) - 3
                    for i in range(2, length ):
                        s = line_lst[i]
                        ss = {s: []}
                        self.REF_CLO.update(ss) ; self.dREF_CLO.update(ss)
                        self.REF_CLO_str.append(s) ;self.REF_CLO_DI.update(ss)
                if line_str[-19:] == 'SYS/#/REF OPE TYPES':
                    length = len(line_lst) - 3
                    for i in range(2, length ):
                        s = line_lst[i]
                        ss = {s: []}
                        self.REF_OPE.update(ss) ; self.dREF_OPE.update(ss)
                        self.REF_OPE_str.append(s) ;self.REF_OPE_DI.update(ss)
                if line_str[-17:] == 'TIME OF FIRST CLO':
                    self.CLO_begin_time = line_lst[0] + '-' + line_lst[1] + '-' + line_lst[2] + ' ' + line_lst[3] + ':' + line_lst[4] + ':' + line_lst[5]
                    self.timetype = line_lst[-5]
                if line_str[-16:] == 'TIME OF LAST CLO':
                    self.CLO_end_time = line_lst[0] + '-' + line_lst[1] + '-' + line_lst[2] + ' ' + line_lst[3] + ':' + line_lst[4] + ':' + line_lst[5]
                if line_str[-17:] == 'TIME OF FIRST OPE':
                    self.OPE_begin_time = line_lst[0] + '-' + line_lst[1] + '-' + line_lst[2] + ' ' + line_lst[3] + ':' + line_lst[4] + ':' + line_lst[5]
                if line_str[-16:] == 'TIME OF LAST OPE':
                    self.OPE_end_time = line_lst[0] + '-' + line_lst[1] + '-' + line_lst[2] + ' ' + line_lst[3] + ':' + line_lst[4] + ':' + line_lst[5]        
                
                if line_str[-13:]=='END OF HEADER':
                    self.line_of_head = num
                    #头文件行数
                if line_str[-16:] == 'START OF OBS CLO':
                    self.line_of_CLO_start = num
                    #CLO内容开始行数
                if line_str[-14:] == 'END OF OBS CLO':
                    self.line_of_CLO_end = num
                    #CLO内容结束行数
                if line_str[-16:] == 'START OF OBS OPE':
                    self.line_of_OPE_start = num
                    #OPE内容开始行数
                if line_str[-14:] == 'END OF OBS OPE':
                    self.line_of_OPE_end = num   
                        #OPE内容阶数行数
        
        '''
        ==================
        读取闭环数据
        ==================
        '''
        
        with open(filename, 'r') as f: 
            read_all = f.readlines() 
            for read_line in read_all[self.line_of_CLO_start+1 : self.line_of_CLO_end]:
                line_lst = read_line.split() 
                line_str= read_line.rstrip()
                
                if line_str[0] == r'>':
                    self.CLO_time['year'].append(float(line_lst[1]))
                    self.CLO_time['month'].append(float(line_lst[2]))
                    self.CLO_time['day'].append(float(line_lst[3]))
                    self.CLO_time['hour'].append(float(line_lst[4]))
                    self.CLO_time['mintes'].append(float(line_lst[5]))
                    self.CLO_time['sec'].append(float(line_lst[6]))
                    self.CLO_time['time'].append(str('%4d' % int(line_lst[1])) + '-' + str('%02d' % int(line_lst[2])) + '-' + str(
                        '%02d' % int(line_lst[3])) + ' ' + str('%02d' % int(line_lst[4])) + ':' + str(
                        '%02d' % int(line_lst[5])) + ':' + str('%2.2f' % float(line_lst[6][0:5])))
                if line_str[:3] == str(self.sat1):
                    '''
                    这里的潜在问题是如果卫星编号大于99那就不能用了
                    最好使用line，而不是lines
                    但是会出现G02-100063911.059 没有空格的情况
                    '''
                    # line = line_str[3:].split()
                    line_lst_new = read_line[3:].split()
                    # print(len(self.OCC_CLO_str) , len(line_lst_new))
                    # print(self.OCC_CLO_str)
                    for i in range(len(self.OCC_CLO_str)):
                        self.OCC_CLO[self.OCC_CLO_str[i]].append(float(line_lst_new[i]))
                        
                if line_str[:3] == str(self.sat2):
                    line_lst_new = read_line[3:].split()
                    for i in range(len(self.REF_CLO_str)):
                        self.REF_CLO[self.REF_CLO_str[i]].append(float(line_lst_new[i]))
                    
                # else:
                #     continue
        
        '''
        ==================
        读取开环数据
        ==================
        '''     
        with open(filename, 'r') as f: 
            read_all = f.readlines() 
            for read_line in read_all[self.line_of_OPE_start+1 : self.line_of_OPE_end]:
                line_lst = read_line.split() 
                line_str= read_line.rstrip()
                
                if line_str[0] == r'>':
                    self.OPE_time['year'].append(float(line_lst[1]))
                    self.OPE_time['month'].append(float(line_lst[2]))
                    self.OPE_time['day'].append(float(line_lst[3]))
                    self.OPE_time['hour'].append(float(line_lst[4]))
                    self.OPE_time['mintes'].append(float(line_lst[5]))
                    self.OPE_time['sec'].append(float(line_lst[6]))
                    self.OPE_time['time'].append(str('%4d' % int(line_lst[1])) + '-' + str('%02d' % int(line_lst[2])) + '-' + str(
                        '%02d' % int(line_lst[3])) + ' ' + str('%02d' % int(line_lst[4])) + ':' + str(
                        '%02d' % int(line_lst[5])) + ':' + str('%2.2f' % float(line_lst[6][0:5])))
                elif line_lst[0] == self.sat1:
                    '''
                    这里的潜在问题是如果卫星编号大于99那就不能用了
                    最好使用line，而不是lines
                    '''
                    line = line_str[3:].split()
                    for i in range(len(self.OCC_OPE_str)):
                        self.OCC_OPE[self.OCC_OPE_str[i]].append(float(line[i]))
                        
                elif line_lst[0] == self.sat2:
                    line = line_str[3:].split()
                    for i in range(len(self.REF_OPE_str)):
                        self.REF_OPE[self.REF_OPE_str[i]].append(float(line[i]))
                    
                else:
                    continue
                
        '''
        ==================
        文件数据读取完毕
        ==================
        '''
        if len(self.CLO_time['time']) > 0:
            self.CLO_time_list = pd.DatetimeIndex(self.CLO_time['time'])
            #CLO_time['time'] 是一个字符串列表，其中包含格式为 'YYYY-MM-DD HH:MM:SS.SS' 的时间戳
            
            self.CLO_dif = np.diff( self.CLO_time_list ).astype(float)/1000000000
            #np.diff 会返回一个数组(array)，表示相邻时间戳之间的时间差，单位为纳秒。  /1e9
        if len(self.OPE_time['time']) > 0:
            self.OPE_time_list = pd.DatetimeIndex(self.OPE_time['time'])
            self.OPE_dif = np.diff( self.OPE_time_list ).astype(float)/1000000000
        
        self.CLO_time_length = len(self.CLO_time_list)
        self.OPE_time_length = len(self.OPE_time_list)
        
        if self.SETTING == 0:
            self.label_kb = 'RISING'
        if self.SETTING == 1:
            self.label_kb = 'SETTING'
            
        for i in range(len(self.OCC_CLO_str)):
            s=self.OCC_CLO_str[i]
            if s[0] == 'L':
                self.OCC_CLO_L.append(s)

                #频率列表和OCC_CLO_L同序
            elif s[0] == 'C':
                self.OCC_CLO_C.append(s)
            elif s[0] == 'S':
                self.OCC_CLO_S.append(s) 
 
                
        for i in range(len(self.OCC_OPE_str)):
            s=self.OCC_OPE_str[i]
            if s[0] == 'L':
                self.OCC_OPE_L.append(s)

            elif s[0] == 'C':
                self.OCC_OPE_C.append(s)
            elif s[0] == 'O':
                self.OCC_OPE_O.append(s)
                
            elif s[0] == 'I':
                self.OCC_OPE_I.append(s)
            elif s[0] == 'Q':
                self.OCC_OPE_Q.append(s)
            elif s[0] == 'S':
                self.OCC_OPE_S.append(s) 

        
        for i in range(len(self.REF_CLO_str)):
            s=self.REF_CLO_str[i]
            if s[0] == 'L':
                self.REF_CLO_L.append(s)

            elif s[0] == 'C':
                self.REF_CLO_C.append(s)

        for i in range(len(self.REF_OPE_str)):
            s=self.REF_OPE_str[i]
            if s[0] == 'L':
                self.REF_OPE_L.append(s)

            elif s[0] == 'C':
                self.REF_OPE_C.append(s)
        
        
        

        
        
        
        '''
        ================================
        过滤数据，保留信噪比大于等于SNR的数据
        只需过滤OCC数据即可
        '''
        
        
        '''
        需要在OCC_OPE字典中加入残差O-L
        '''
    def SNR_filter(self,SNR_lim1=40,SNR_lim2=40,window_CLO=30,window_OPE=60):
        '''
        根据信噪比筛选数据，
        将信噪比信息作滑动平均，窗口为1秒种：闭环为30个，开环为60个
        如果该处的信噪比值小于 SNR_lim，则之后的数据统统不要
        '''
        self.OCC_CLO_filter = copy.deepcopy(self.OCC_CLO)
        self.OCC_OPE_filter = copy.deepcopy(self.OCC_OPE)

        '''
        组合
        '''
              
        '''
        ===============
        '''
        index_CLO = [] ; index_OPE=[]
        for tag in self.OCC_CLO_S:
            SNR = tag

            '''
            找到SNR_AVE小于等于界限的索引
            '''
            # if len(dict(self.OCC_CLO[SNR])) == 0:
            #     self.OCC_
            # windows_CLO = 30
            average = vector_moving_average(self.OCC_CLO[SNR] , window_CLO)
            
            index_ = find_first_less_or_equal(average , SNR_lim1)

            if index_ == 0 :
                #如果index_=0并且列表还不为空的话：两种情况
                #一是截取时间过短，可以用file_edit
                #二是接收的数据有问题，中间有部分变化值
                L = "L"+SNR[1:]
                C = "C"+SNR[1:]
                self.OCC_CLO_filter[SNR] = np.array(self.OCC_CLO_filter[SNR], dtype=np.float64)
                self.OCC_CLO_filter[L] = np.array(self.OCC_CLO_filter[L], dtype=np.float64)
                self.OCC_CLO_filter[C] = np.array(self.OCC_CLO_filter[C], dtype=np.float64)
                self.OCC_CLO_filter[SNR][:] = np.nan
                self.OCC_CLO_filter[L][:] = np.nan
                self.OCC_CLO_filter[C][:] = np.nan
                continue
            index_CLO.append(index_)
            

        if len(index_CLO)==0:
            index_CLO_min = -1
        else:
            index_CLO_min = min(index_CLO)

        
        
        for tag in self.OCC_CLO_filter:

            # '''
            # 找到SNR_AVE小于等于界限的索引
            # '''
            self.OCC_CLO_filter[tag] = np.array(self.OCC_CLO_filter[tag], dtype=np.float64)
            self.OCC_CLO_filter[tag][index_CLO_min:] = np.nan
            # self.dOCC_CLO[tag][index_CLO_min:] = np.nan

        
        for tag in self.OCC_OPE_S:
            SNR = tag

            '''
            找到SNR_AVE小于等于界限的索引
            '''
            # windows_OPE = 60
            average = vector_moving_average(self.OCC_OPE[SNR] , window_OPE)

            index_ = find_first_less_or_equal(average , SNR_lim2)

            if index_ == 0 :

                #如果index_=0并且列表还不为空的话：两种情况
                #一是截取时间过短，可以用file_edit
                #二是接收的数据有问题，中间有部分变化值
                L = "L"+SNR[1:]
                C = "C"+SNR[1:]
                O = "O"+SNR[1:]
                I = "I"+SNR[1:]
                Q = "Q"+SNR[1:]
                self.OCC_OPE_filter[SNR] = np.array(self.OCC_OPE_filter[SNR], dtype=np.float64)
                self.OCC_OPE_filter[L] = np.array(self.OCC_OPE_filter[L], dtype=np.float64)
                self.OCC_OPE_filter[C] = np.array(self.OCC_OPE_filter[C], dtype=np.float64)
                self.OCC_OPE_filter[O] = np.array(self.OCC_OPE_filter[O], dtype=np.float64)
                self.OCC_OPE_filter[I] = np.array(self.OCC_OPE_filter[I], dtype=np.float64)
                self.OCC_OPE_filter[Q] = np.array(self.OCC_OPE_filter[Q], dtype=np.float64)
                self.OCC_OPE_filter[SNR][:] = np.nan
                self.OCC_OPE_filter[L][:] = np.nan
                self.OCC_OPE_filter[C][:] = np.nan
                self.OCC_OPE_filter[O][:] = np.nan
                self.OCC_OPE_filter[I][:] = np.nan
                self.OCC_OPE_filter[Q][:] = np.nan
                
                continue
            
            index_OPE.append(index_)
        if len(index_OPE)==0:
            index_OPE_min = -1
        else:
            index_OPE_min = min(index_OPE)

        for tag in self.OCC_OPE_filter:

            '''
            找到SNR_AVE小于等于界限的索引
            '''
 
            self.OCC_OPE_filter[tag] = np.array(self.OCC_OPE_filter[tag], dtype=np.float64)
            self.OCC_OPE_filter[tag][index_OPE_min:] = np.nan

        if index_CLO_min == len(self.CLO_time_list):
            self.filter_CLO_end_time = self.CLO_time_list[-1]    
        else:
            self.filter_CLO_end_time = self.CLO_time_list[index_CLO_min]
        if index_OPE_min == len(self.OPE_time_list):
            self.filter_OPE_end_time = self.OPE_time_list[-1]    
        else:
            self.filter_OPE_end_time = self.OPE_time_list[index_OPE_min]
        '''
        变化率
        '''
        for i in range(len(self.OCC_CLO_str)):
            s=self.OCC_CLO_str[i]
            self.dOCC_CLO[s]= np.diff(self.OCC_CLO_filter[s])/self.CLO_dif

        for i in range(len(self.OCC_OPE_str)):
            s=self.OCC_OPE_str[i]
            self.dOCC_OPE[s]= np.diff(self.OCC_OPE_filter[s])/self.OPE_dif
            
        for i in range(len(self.REF_CLO_str)):
            s=self.REF_CLO_str[i]
            self.dREF_CLO[s]= np.diff(self.REF_CLO[s])/self.CLO_dif

        for i in range(len(self.REF_OPE_str)):
            s=self.REF_OPE_str[i]
            self.dREF_OPE[s]= np.diff(self.REF_OPE[s])/self.OPE_dif
        
        
        '''
        组合
        '''
        for i in range(len(self.OCC_CLO_L)):
           si = self.OCC_CLO_L[i]
           fi = find_frequence(si[1:],self.sat1)
           Pi = np.array(self.OCC_CLO_filter[si]) ; Ci = np.array(self.OCC_CLO_filter['C'+si[1:]])
           self.OCC_CLO_DIF.update({si:[]}) 
           if si in self.REF_CLO_L:
               
               self.OCC_CLO_DIF[si] = DIF_COMB(Pi , self.REF_CLO[si])
               # plt.plot(self.OCC_CLO_DIF[si])
           for  j in range(i+1,len(self.OCC_CLO_L)):
               sj = self.OCC_CLO_L[j]
               fj = find_frequence(sj[1:],self.sat1)
               Pj = np.array(self.OCC_CLO_filter[sj]) ; Cj = np.array(self.OCC_CLO_filter['C'+sj[1:]])

               LL = si[1:]+sj[1:] 
               
               
               self.OCC_CLO_MW.update({LL:[]})  ; self.OCC_CLO_MW[LL] = MW_COMB(Pi,Pj,Ci,Cj,fi,fj)
               self.OCC_CLO_GF.update({LL:[]})  ; self.OCC_CLO_GF[LL] = GF_COMB_2(Pi, Pj, fi, fj)
               self.OCC_CLO_IF.update({LL:[]})  ; self.OCC_CLO_IF[LL] = IF_COMB(Pi, Pj, fi, fj)
               # self.OCC_CLO_IF.update({LLC2:[]}); self.OCC_CLO_IF[LLC2] = IF_COMB(Pi, Pj, Cj, fi, fj)
               
               # plt.plot(self.OCC_CLO_MW[LL])

       
       
        for i in range(len(self.REF_CLO_L)):
           si = self.REF_CLO_L[i]
           fi = find_frequence(si[1:],self.sat2)
           Pi = np.array(self.REF_CLO[si]) ; Ci = np.array(self.REF_CLO['C'+si[1:]])
           

           for  j in range(i+1,len(self.REF_CLO_L)):
               sj = self.REF_CLO_L[j]
               fj = find_frequence(sj[1:],self.sat2)
               Pj = np.array(self.REF_CLO[sj]) ; Cj = np.array(self.REF_CLO['C'+sj[1:]])
               LL = si[1:]+sj[1:]
               
               
               self.REF_CLO_MW.update({LL:[]})  ; self.REF_CLO_MW[LL] = MW_COMB(Pi,Pj,Ci,Cj,fi,fj)
               self.REF_CLO_GF.update({LL:[]})  ; self.REF_CLO_GF[LL] = GF_COMB_2(Pi, Pj, fi, fj)
               self.REF_CLO_IF.update({LL:[]})  ; self.REF_CLO_IF[LL] = IF_COMB(Pi, Pj, fi, fj)
               # self.REF_CLO_IF.update({LLC2:[]}); self.REF_CLO_IF[LLC2] = IF_COMB(Pi, Pj, Cj, fi, fj)


       
        for i in range(len(self.OCC_OPE_L)):
           si = self.OCC_OPE_L[i]
           fi = find_frequence(si[1:],self.sat1)
           Pi = np.array(self.OCC_OPE_filter[si]) ; Ci = np.array(self.OCC_OPE_filter['C'+si[1:]])
           
           self.OCC_OPE_DIF.update({si:[]}) 
           if si in self.REF_OPE_L:
               
               self.OCC_OPE_DIF[si] = DIF_COMB(Pi , self.REF_OPE[si])
               # plt.plot(self.OCC_OPE_DIF[si])
           for  j in range(i+1,len(self.OCC_OPE_L)):
               sj = self.OCC_OPE_L[j]
               fj = find_frequence(sj[1:],self.sat1)
               Pj = np.array(self.OCC_OPE_filter[sj]) ; Cj = np.array(self.OCC_OPE_filter['C'+sj[1:]])
               LL = si[1:]+sj[1:] 
               
               
               self.OCC_OPE_MW.update({LL:[]})  ; self.OCC_OPE_MW[LL] = MW_COMB(Pi,Pj,Ci,Cj,fi,fj)
               self.OCC_OPE_GF.update({LL:[]})  ; self.OCC_OPE_GF[LL] = GF_COMB_2(Pi, Pj, fi, fj)
               self.OCC_OPE_IF.update({LL:[]})  ; self.OCC_OPE_IF[LL] = IF_COMB(Pi, Pj, fi, fj)
               # self.OCC_OPE_IF.update({LLC2:[]}); self.OCC_OPE_IF[LLC2] = IF_COMB(Pi, Pj, Cj, fi, fj)
               
       
        for i in range(len(self.REF_OPE_L)):
           si = self.REF_OPE_L[i]
           fi = find_frequence(si[1:],self.sat2)
           Pi = np.array(self.REF_OPE[si]) ; Ci = np.array(self.REF_OPE['C'+si[1:]])


           for  j in range(i+1,len(self.REF_OPE_L)):
               sj = self.REF_OPE_L[j]
               fj = find_frequence(sj[1:],self.sat2)
               Pj = np.array(self.REF_OPE[sj]) ; Cj = np.array(self.REF_OPE['C'+sj[1:]])
               LL = si[1:]+sj[1:] ; LLC1 = si[1:]+sj[1:] + si[1:] ; LLC2 = si[1:]+sj[1:] + sj[1:]
               
               
               self.REF_OPE_MW.update({LL:[]})  ; self.REF_OPE_MW[LL] = MW_COMB(Pi,Pj,Ci,Cj,fi,fj)
               self.REF_OPE_GF.update({LL:[]})  ; self.REF_OPE_GF[LL] = GF_COMB_2(Pi, Pj, fi, fj)
               self.REF_OPE_IF.update({LL:[]})  ; self.REF_OPE_IF[LL] = IF_COMB(Pi, Pj, fi, fj)
               # self.REF_OPE_MP.update({LLC2:[]}); self.REF_OPE_MP[LLC2] = IF_COMB(Pi, Pj, Cj, fi, fj)
    
    def DI_CHECK(self ):
        CLO_time_full = pd.date_range(
        start=self.CLO_begin_time,
        end=str(self.filter_CLO_end_time),
        freq='20ms'  # 20毫秒 = 0.02秒
        )
        
        OPE_time_full = pd.date_range(
        start=self.OPE_begin_time,
        end=str(self.filter_OPE_end_time),
        freq='10ms'  # 20毫秒 = 0.02秒
        )
        
        self.missing_time_CLO = CLO_time_full.difference(self.CLO_time_list)
        self.missing_time_OPE = OPE_time_full.difference(self.OPE_time_list)
        
        for tag in self.OCC_CLO_DI:
            self.OCC_CLO_DI[tag] = 1-len(self.missing_time_CLO)/len(CLO_time_full)
            
        for tag in self.REF_CLO_DI:
            self.REF_CLO_DI[tag] = 1-len(self.missing_time_CLO)/len(CLO_time_full)
            
        for tag in self.OCC_OPE_DI:
            self.OCC_OPE_DI[tag] =  1-len(self.missing_time_OPE)/len(OPE_time_full)
        for tag in self.REF_OPE_DI:
            self.REF_OPE_DI[tag] = 1-len(self.missing_time_OPE)/len(OPE_time_full)
        
        self.OCC_CLO_bad_data = {}     #时间 + 缺失数据标符 
        self.REF_CLO_bad_data ={}
        self.OCC_OPE_bad_data = {}
        self.REF_OPE_bad_data ={}
        
        for i in range(len(self.missing_time_CLO)):
            time_tag = self.missing_time_CLO[i]
            self.OCC_CLO_bad_data[time_tag] = self.OCC_CLO_str
            self.REF_CLO_bad_data[time_tag] = self.REF_CLO_str

        
        for i in range(len(self.missing_time_OPE)):
            time_tag = self.missing_time_OPE[i]
            self.OCC_OPE_bad_data[time_tag] = self.OCC_OPE_str
            self.REF_OPE_bad_data[time_tag] = self.REF_OPE_str
        
        
    def write_DI(self):
        '''
        将信息写入LOG文件
        包括：
        检测文件
        文件类型
        数据完整度，四个
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
            file.write('file type: A\n')
            file.write('\n')
            file.write(f'{self.sat1}_CLO_DATA_INTEGRETY \n')
            for tag in self.OCC_CLO_DI:
                file.write(f'{tag}: {self.OCC_CLO_DI[tag] * 100:.2f}%\n')
            
            file.write('\n')
            file.write(f'{self.sat2}_CLO_DATA_INTEGRETY \n')
            for tag in self.REF_CLO_DI:
                file.write(f'{tag}: {self.REF_CLO_DI[tag] * 100:.2f}%\n')
            
            file.write('\n')    
            file.write(f'{self.sat1}_OPE_DATA_INTEGRETY \n')
            for tag in self.OCC_OPE_DI:
                file.write(f'{tag}: {self.OCC_OPE_DI[tag] * 100:.2f}%\n')
            
            file.write('\n')    
            file.write(f'{self.sat2}_OPE_DATA_INTEGRETY \n')
            for tag in self.REF_OPE_DI:
                file.write(f'{tag}: {self.REF_OPE_DI[tag] * 100:.2f}%\n')
            # 读取文件内容
            file.write('\n')
            if not self.missing_time_CLO.empty:
                file.write('START OF OBS CLO\n')
                for time_tag in self.missing_time_CLO:
                        file.write(f'TIME {time_tag} \n')
                        file.write(f'{self.sat1}  {self.OCC_CLO_bad_data[time_tag]} \n')
                        file.write(f'{self.sat2}  {self.REF_CLO_bad_data[time_tag]} \n')
                file.write('END OF OBS CLO\n \n')
            if not self.missing_time_OPE.empty:
                file.write('START OF OBS OPE \n')
                for time_tag in self.missing_time_OPE:
                        file.write(f'TIME {time_tag} \n')
                        file.write(f'{self.sat1}  {self.OCC_OPE_bad_data[time_tag]} \n')
                        file.write(f'{self.sat2}  {self.REF_OPE_bad_data[time_tag]} \n')
                file.write('END OF OBS OPE')  
        
        
        # Show_file(file_to_write)  
        return file_to_write
    
        # print(len(self.OCC_CLO_str) ,len(self.CLO_time_list) )
    def Edit_Atm(self,input_filename,start_time_CLO,end_time_CLO , start_time_OPE,end_time_OPE ,output_filename):
        '''
        写入 OCC CLO :问题是还是得写入REF星吧，都写一个函数吧
        先处理异常情况：
        ①start_time不在内
        ②end_time  不在
        ④时间戳格式不对头
        '''
        if output_filename[-4:]!='.ROX':
            output_filename = output_filename+'.ROX'
            
        s_time_CLO = pd.Timestamp(start_time_CLO)
        e_time_CLO = pd.Timestamp(end_time_CLO)
        in_s_time_CLO = s_time_CLO in self.CLO_time_list
        in_e_time_CLO = e_time_CLO in self.CLO_time_list
        
        s_time_OPE = pd.Timestamp(start_time_OPE)
        e_time_OPE = pd.Timestamp(end_time_OPE)
        in_s_time_OPE = s_time_OPE in self.OPE_time_list
        in_e_time_OPE = e_time_OPE in self.OPE_time_list
        
 
        
        warning = ''
        '''
        异常处理
        得到 warning信息，然后在app内以警告框形式呈现
        '''
        if not in_s_time_CLO:
           warning = 'CLO start time entered is not within the valid time range'
           return False,warning   
          
        if not in_e_time_CLO:
           warning = 'CLO end time entered is not within the valid time range'
           return False,warning
            
 
        
 
        if not is_valid_datetime(start_time_CLO):
           warning = 'CLO start time does not meet the required time format'  
           return False,warning
        if not is_valid_datetime(end_time_CLO):
           warning = 'CLO end time does not meet the required time format'
           return False,warning
       
        if not in_s_time_OPE:
           warning = 'OPE start time entered is not within the valid time range'
           return False,warning   
          
        if not in_e_time_OPE:
           warning = 'OPE end time entered is not within the valid time range'
           return False,warning
            
        if not is_valid_datetime(start_time_OPE):
           warning = 'OPE start time does not meet the required time format'  
           return False,warning
        if not is_valid_datetime(end_time_OPE):
           warning = 'OPE end time does not meet the required time format'
           return False,warning
        
        '''
        异常处理
        '''       
        shutil.copy(input_filename,output_filename)
        with open(output_filename, 'r') as f: 
            lines = f.readlines()
        
        processed_lines = []
        start_datetime_CLO = datetime.strptime(start_time_CLO, "%Y-%m-%d %H:%M:%S.%f")
        end_datetime_CLO   = datetime.strptime(end_time_CLO, "%Y-%m-%d %H:%M:%S.%f")
        start_datetime_OPE = datetime.strptime(start_time_OPE, "%Y-%m-%d %H:%M:%S.%f")
        end_datetime_OPE   = datetime.strptime(end_time_OPE, "%Y-%m-%d %H:%M:%S.%f")
        
 
        for read_line in lines[:self.line_of_head + 2]:  #包涵了START OF OBS CLO
            '''
            处理头文件
            '''
            line_str= read_line.rstrip()
 
            
            '''
             处理时间
            '''
            if line_str[-17:] == 'TIME OF FIRST CLO':
                microsecond = start_datetime_CLO.microsecond * 10  
 
                # 格式化秒和微秒，确保微秒是7位
                formatted_second = f"{start_datetime_CLO.second:2d}.{microsecond:07d}"
                new_line = f"  {start_datetime_CLO.year:4d}    {start_datetime_CLO.month:2d}    {start_datetime_CLO.day:2d}    {start_datetime_CLO.hour:2d}    {start_datetime_CLO.minute:2d}   {formatted_second}     GPS         TIME OF FIRST CLO\n"
                processed_lines.append(new_line)
                # pass
            elif line_str[-16:] == 'TIME OF LAST CLO':
                microsecond = end_datetime_CLO.microsecond * 10 
                # 格式化秒和微秒，确保微秒是7位
                formatted_second = f"{end_datetime_CLO.second:2d}.{microsecond:07d}"
                new_line = f"  {end_datetime_CLO.year:4d}    {end_datetime_CLO.month:2d}    {end_datetime_CLO.day:2d}    {end_datetime_CLO.hour:2d}    {end_datetime_CLO.minute:2d}   {formatted_second}     GPS         TIME OF LAST CLO\n"
                processed_lines.append(new_line)
                
                
            elif line_str[-17:] == 'TIME OF FIRST OPE':
                microsecond = start_datetime_OPE.microsecond * 10  
 
                # 格式化秒和微秒，确保微秒是7位
                formatted_second = f"{start_datetime_OPE.second:2d}.{microsecond:07d}"
                new_line = f"  {start_datetime_OPE.year:4d}    {start_datetime_OPE.month:2d}    {start_datetime_OPE.day:2d}    {start_datetime_OPE.hour:2d}    {start_datetime_OPE.minute:2d}   {formatted_second}     GPS         TIME OF FIRST OPE\n"
                processed_lines.append(new_line)
                # pass
            elif line_str[-16:] == 'TIME OF LAST OPE':
                microsecond = end_datetime_OPE.microsecond * 10 
                # 格式化秒和微秒，确保微秒是7位
                formatted_second = f"{end_datetime_OPE.second:2d}.{microsecond:07d}"
                new_line = f"  {end_datetime_OPE.year:4d}    {end_datetime_OPE.month:2d}    {end_datetime_OPE.day:2d}    {end_datetime_OPE.hour:2d}    {end_datetime_OPE.minute:2d}   {formatted_second}     GPS         TIME OF LAST OPE\n"
                processed_lines.append(new_line) 
            
            #用于匹配初始时间
            else:
                processed_lines.append(line_str+'\n')
                
        for index ,read_line in enumerate(lines[:self.line_of_CLO_end+1]):
            '''
            找到时间戳对应CLO
            '''
            line_str= read_line.rstrip()
            if line_str[0] == r'>':
                timestamp_str = read_line[1:].strip().split()[0:6]
                
                ts_str = f"{timestamp_str[0]} {timestamp_str[1]} {timestamp_str[2]} {timestamp_str[3]} {timestamp_str[4]} {timestamp_str[5][:-1]}"
                #%.f表示微妙范围为 0 - 999999，但是atm文件中给了七位小数
                   # 转换为 datetime 对象       
                current_datetime = datetime.strptime(ts_str, "%Y %m %d %H %M %S.%f")
                if start_datetime_CLO == current_datetime:
                    start_CLO = index 
                    # print(index)
                if end_datetime_CLO  == current_datetime:   
                    end_CLO = index  
                    # print(index)
               
        for index ,read_line in enumerate(lines[self.line_of_CLO_end+1:self.line_of_OPE_end+1]):
            '''
            找到时间戳对应OPE
            '''
            line_str= read_line.rstrip()
            if line_str[0] == r'>':
                timestamp_str = read_line[1:].strip().split()[0:6]
                
                ts_str = f"{timestamp_str[0]} {timestamp_str[1]} {timestamp_str[2]} {timestamp_str[3]} {timestamp_str[4]} {timestamp_str[5][:-1]}"
                #%.f表示微妙范围为 0 - 999999，但是atm文件中给了七位小数
                   # 转换为 datetime 对象       
                current_datetime = datetime.strptime(ts_str, "%Y %m %d %H %M %S.%f")
            if start_datetime_OPE == current_datetime:
                start_OPE = index + self.line_of_CLO_end-1
                # print(index)
            if end_datetime_OPE  == current_datetime:
                end_OPE = index  + self.line_of_CLO_end-1
        
 
 
        for index in range(start_CLO , end_CLO+3 , 3):
            processed_lines.append(lines[index])
            processed_lines.append(lines[index+1])
            processed_lines.append(lines[index+2])
            
        processed_lines.append(lines[self.line_of_CLO_end].rstrip()+'\n')
        processed_lines.append(lines[self.line_of_OPE_start].rstrip()+'\n')
        
        for index in range(start_OPE , end_OPE+2 , 3):
            processed_lines.append(lines[index])
            processed_lines.append(lines[index+1])
            processed_lines.append(lines[index+2])   
            
        processed_lines.append(lines[self.line_of_OPE_end].rstrip()) 
       

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

        return True , warning
   
if __name__ == "__main__":   
    filename=r"C:\Users\zhangmingyi24\OneDrive\Desktop\ROEX分析软件开源程序论文\ROEX分析软件开源程序论文\ROEX分析软件代码\PyROEX_论文\data\cloAtm_GNOS.007.G02.06.2024.152.38667.0115.03.0000_bin.ROX"
    # filename=r"C:\Users\zhangmingyi24\OneDrive\Desktop\ROEX分析软件开源程序论文\ROEX分析软件开源程序论文\ROEX分析软件代码\PyROEX\data\processed_atm.ROX"
    # filename=r"C:\Users\zhangmingyi24\OneDrive\Desktop\ROEX分析软件开源程序论文\ROEX分析软件开源程序论文\ROEX分析软件代码\PyROEX\data\processed_atm - 副本.ROX"
    test =Atm_File()
    test.read_file(filename)
    test.SNR_filter(40,40)
    test.DI_CHECK()
    test.write_DI()
    outfile_name = "processed_atm"
    jug,warning = test.Edit_Atm(filename, '2024-5-31 10:44:40.00', '2024-5-31 10:46:21.98','2024-5-31 10:45:19.00', '2024-5-31 10:46:21.99',outfile_name)
    # 
            