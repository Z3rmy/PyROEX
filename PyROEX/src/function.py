# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 10:48:25 2025

@author: 22185
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
from matplotlib.ticker import AutoLocator

def time_formatter(x, pos):
    # 将数值转换为 datetime 对象
    dt = mdates.num2date(x)
    
    # 提取微秒并四舍五入到两位小数
    ms_rounded = round(dt.microsecond / 10000)  # 将微秒转换为两位小数（除以10000）
    # 处理四舍五入后可能的溢出（如999.99微秒 → 100 → 秒进位）
    if ms_rounded >= 100:
        dt = dt + pd.Timedelta(seconds=1)  # 若需要严格处理进位，可添加此逻辑
        ms_rounded = 0
    
    # 格式化为 HH:MM:SS.ss
    return dt.strftime('%H:%M:%S.') + f"{ms_rounded:02d}"



c = 299792458  #m/s


def jug_A_or_I(filename):
    A_or_I = 'none'  # 默认值
    try:
        with open(filename, 'r') as f:
            first_line_lst = f.readline().split()
            # 确保至少有两个元素
            if len(first_line_lst) > 1:
                if first_line_lst[1] == 'A':
                    A_or_I = 'A'
                elif first_line_lst[1] == 'I':
                    A_or_I = 'I'
                else:
                    A_or_I = 'none'  # 如果不为 'A' 或 'I'，返回 None
            else:
                A_or_I = 'none'  # 如果文件第一行格式不正确
    except Exception:
        return A_or_I  # 出现任何异常时返回 None
    return A_or_I


def A_V(data , j): #j: 从索引j开始重新计算
    '''
    目的：利用递推求取从索引j开始的平均值和方差矩阵
         利于周跳时重新划分弧段
    '''
    A_n_1 = data[j]   #A: average
    var_n_1   = 0
    V2 = [var_n_1]  ; A = [A_n_1]
    n = 2
    k = j+1 
    for i in range(j+1,len(data)):
        N_n       = data[k]
        A_n   = A_n_1 + (N_n - A_n_1)/n
        var_n   = (n-1)/n/n * (N_n - A_n_1)**2 + (n-1)/n*var_n_1     #(n-1)/n/n
        V2.append(var_n) 
        A.append(A_n)
        var_n_1 = var_n ; A_n_1 = A_n
        
        n=n+1; k=k+1
        
    return A , V2

frequence_BDS = {
    ('2I', '2Q', '2X')                                               : [1561.098],
    ('1D', '1P', '1X','1S', '1L', '1Z')                              : [1575.42] ,  
    ('5D','5P','5X')                                                 : [1176.45] ,
    ('7I','7Q','7X','7D','7P','7Z')                                  : [1207.140],
    ('8D','8P','8X')                                                 : [1191.795],
    ('6I','6Q','6X','6D','6P','6Z')                                  : [1268.52] ,
    ('2C','2D','2S','2L','2X','2P','2W','2Y','2M','2N')              : [1227.60] 
}  #MHz

frequence_GPS = {
    ('1C','1S','1L','1X','1P','1W','1Y','1M','1N')                   : [1575.42] ,  
    ('2C','2D','2S','2L','2X','2P','2W','2Y','2M','2N')              : [1227.60] ,
    ('5I','5Q','5X')                                                 : [1176.45],
}  #MHz


k_GLO = 5
frequence_GLO = {
    ('1C','1P')                                                      : [1602+k_GLO*9/16] ,  
    ('4A','4B','4X')                                                 : [1600.995] ,
    ('2C','2P')                                                      : [1246+k_GLO*7/16],
    ('6A','6B','6X')                                                 : [1248.06],
    ('3I','3Q','3X')                                                 : [1202.025],
}  #MHz

frequence_GAL = {
    ('1A','1B','1C','1X','1Z')                                       : [1575.42] ,  
    ('5I','5Q','5X')                                                 : [1176.45 ] ,
    ('7I','7Q','7X')                                                 : [1207.140],
    ('8I','8Q','8X')                                                 : [1191.795],
    ('6A','6B','6C','6X','6Z')                                       : [1278.75 ],
}  #MHz
# '1C','1X','1W','1Y','1M','1N'
# '5I','5Q'
# sym = '2I'
frequency_dict = {
    'C': frequence_BDS,
    'G': frequence_GPS,
    'R': frequence_GLO,
    'E': frequence_GAL
}

def find_frequence(string,PRN):

    # 获取对应的频率字典
    frequence = frequency_dict.get(PRN[0])
    
    if frequence is None:
        return None  

    # 遍历字典并查找匹配的字符串
    for k in frequence:
        if string in k:
            return frequence[k][0]

    
def linear_interpolate(a):
    '''
    利用插值方法处理缺失数据的情况
    0 1 0
    1 1 0
    0 0 1
    '''
    # 获取非零元素的索引
    non_zero_indices = np.where(a != 0)[0]
    
    # 遍历0值的位置
    for i in range(len(a)):
        if a[i] == 0:
            # 找到当前位置之前最近的非零元素索引
            prev_index = non_zero_indices[non_zero_indices < i][-1] if np.any(non_zero_indices < i) else None
            # 找到当前位置之后最近的非零元素索引
            next_index = non_zero_indices[non_zero_indices > i][0] if np.any(non_zero_indices > i) else None
            
            if prev_index is None:  # 如果没有前面的非零值，使用后面的非零值
                a[i] = a[next_index]
            elif next_index is None:  # 如果没有后面的非零值，使用前面的非零值
                a[i] = a[prev_index]
            else:  # 使用前后两个非零值进行线性插值
                a[i] = a[prev_index] + (a[next_index] - a[prev_index]) * (i - prev_index) / (next_index - prev_index)
    
    return a




def Show_file(file_to_write):
    with open(file_to_write, 'r') as file:
        file_content = file.read()
    window = tk.Tk()
    window.title("File content display")

    # 创建一个滚动文本框来显示文件内容
    text_area = scrolledtext.ScrolledText(window, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    # 插入文件内容
    text_area.insert(tk.END, file_content)

    # 启动窗口的主循环
    window.mainloop()   
    
    return

def vector_moving_average(vector, window_size=30):
    """
    计算向量中每个值与滑动平均值的差，不使用卷积方法。
    
    参数:
        vector (list or np.ndarray): 输入向量（一维数组）
        window_size (int): 滑动窗口的大小，默认为3
    
    返回:
        np.ndarray: 输入向量与滑动平均值的差值数组
    """
    arr = np.array(vector)
    n = len(arr)
    
    if arr.ndim != 1:
        raise ValueError("Input must be a 1D array or iterable.")
    
    if window_size < 1:
        raise ValueError("Window size must be a positive integer.")
    if window_size > len(arr):
        raise ValueError("Window size cannot exceed the vector length.")
    
    moving_avg = np.zeros(n)
    half_window = window_size // 2
    
    for i in range(n):
        start = max(0, i - half_window)
        end = min(n, i + half_window + 1)  # 窗口的结束索引（不包含）
        window = arr[start:end]
        avg = window.mean()
        moving_avg[i] = avg
    
    res = moving_avg
    
    return res

def find_first_less_or_equal(vector, threshold=40):
    for index, value in enumerate(vector):
        if value < threshold:
            return index
    # 如果所有元素都大于阈值，返回-1或其他标识
    return len(vector)

def is_valid_datetime(datetime_str):
    format_str = "%Y-%m-%d %H:%M:%S.%f"
    
    try:
        datetime.strptime(datetime_str, format_str) 
        return True
    except ValueError:
        return False

def MW_COMB(P1,P2,C1,C2,f1,f2):

    lambda1 = c/(f1*1e6) ; lambda2 =c/(f2*1e6)

    MW = P1-P2-(f1-f2)/(f1+f2)*(C1/lambda1 + C2/lambda2)
    # fig, axs = plt.subplots(1, 1, figsize=(12, 12)) 
    # axs.plot(MW)
    # MW = vector_diff_from_moving_average(MW,window_size=20)
    MW = np.diff(MW,n=1)
    return np.array(MW)

def GF_COMB_2(P1,P2,f1,f2):
    lambda1=c/(f1*1e6) ; lambda2 = c/(f2*1e6)
    L1= lambda1*P1 ; L2 = lambda2*P2 
    GF = L1 - L2
    # GF = P1-P2
    GF = np.diff(GF,n=1)

    # GF1=GF[2:]-GF[1:-1]
    # GF2=GF[1:-1]-GF[:-2]
    # GF3=GF1-GF2
    
    return GF

def GF_COMB_3(P1,P2,P3,f1,f2,f3):
    lambda1=c/(f1*1e6) ; lambda2 = c/(f2*1e6) ;lambda3= c/(f2*1e6)
    L1= lambda1*P1 ; L2 = lambda2*P2 ; L3= lambda3*P3
    a12 = f1**2/(f1**2-f2**2); b12 = -f2**2/(f1**2-f2**2)
    a13 = f1**2/(f1**2-f3**2); b13 = -f3**2/(f1**2-f3**2)
    GF = (a12*L1 + b12*L2) - (a13*L1 + b13*L3)
    GF = np.diff(GF,n=1)
    # GF=GF[2:]-GF[1:-1]
    # GF=GF[1:-1]-GF[:-2]
    
    return GF

def MP_COMB(P1,P2,C1,f1,f2):
    lambda1=c/(f1*1e6) ; lambda2 = c/(f2*1e6) 
    L1= lambda1*P1 ; L2 = lambda2*P2 
    MP = C1 - (f1**2+f2**2)/(f1**2-f2**2)*L1 + 2*(f2**2)/(f1**2-f2**2)*L2
    # MP = vector_diff_from_moving_average(MP,window_size=30)
    return MP

def IOD(P1,P2,f1,f2):   #IF COMB

    lambda1=c/(f1*1e6) ; lambda2 = c/(f2*1e6) 
    L1= lambda1*P1 ; L2 = lambda2*P2 
    
    IOD=f2**2/(f1**2-f2**2)*(L1-L2)
    IOD = np.diff(IOD,n=1)
        
    return IOD



def IF_COMB(P1,P2,f1,f2):   #没有除以时间，需要在后面处理
    if f1==f2:
        return GF_COMB_2(P1, P2, f1, f2)
    lambda1=c/(f1*1e6) ; lambda2 = c/(f2*1e6)
    L1= lambda1*P1 ; L2 = lambda2*P2 

    IF = f1**2/(f1**2-f2**2)*L1 - f2**2/(f1**2-f2**2)*L2
    # IF = f1**2/(f1**2-f2**2)*P1 - f2**2/(f1**2-f2**2)*P2
    IF = np.diff(IF,n=1)
    return IF

def HOD(P,order=4):
    diff_n = np.diff(P,n=order)    
    return diff_n

def DIF_COMB(P1,P2):
    P1 = np.array(P1)
    P2 = np.array(P2)
    
    dif = P1-P2
    dif = np.diff(dif,n=1)
    return dif

#            time_diffs_seconds = np.diff(x).astype('timedelta64[s]').astype(float)  
            # axs[2].plot(x[1:], time_diffs_seconds, '.' ,linewidth=3)