# -*- coding: utf-8 -*-

'''
Created on 24.01.2019

@author: yu03
'''
import numpy as np
from scipy import signal

class Data():
    '''
    Operating Data Files (.txt)
    '''
    def __init__(self):
        '''
        Constructor
        '''
        return
    
    def Read_Data_5Ch(self, name):
        '''
            Return Data in File (5 Channels: Data.Data_Ch1, Data.Data_Ch2, Data.Data_Ch3, Data.Data_Ch4, Data.Data_Ch5)
            File name required (default path)
        '''
        print('Reading Data')
        with open(name,'r') as fid:
            self.line=''
            while self.line[0:4] != '----':
                self.line = fid.readline()
                print(self.line)
                if self.line[0:2] == 'Fs':
                    self.p, self.q, self.m, self.n = self.line.strip().split(' ')
                    self.Fs = float(self.m)
                    print('Fs = %f\n'%self.Fs)
            self.out_str = fid.readlines()
        self.Data_Ch1, self.Data_Ch2, self.Data_Ch3, self.Data_Ch4, self.Data_Ch5, self.Data_Ch6 = [], [], [], [], [], []
        for self.line in self.out_str:
            self.a, self.b, self.c, self.d, self.e = self.line.strip().split(', ')
            self.Data_Ch1.append(float(self.a))
            self.Data_Ch2.append(float(self.b))
            self.Data_Ch3.append(float(self.c))
            self.Data_Ch4.append(float(self.d))    
            self.Data_Ch5.append(float(self.e))
#             self.Data_Ch6.append(float(self.f))
        
        self.Data_Ch1 = np.array(self.Data_Ch1)
        self.Data_Ch2 = np.array(self.Data_Ch2)
        self.Data_Ch3 = np.array(self.Data_Ch3)
        self.Data_Ch4 = np.array(self.Data_Ch4)
        self.Data_Ch5 = np.array(self.Data_Ch5)
#         self.Data_Ch6 = np.array(self.Data_Ch6)
        
        return self.Data_Ch1, self.Data_Ch2, self.Data_Ch3, self.Data_Ch4, self.Data_Ch5, self.Data_Ch6, self.Fs
    
    
    def Read_Data_3Ch(self, name):
        '''
            Return Data in File (5 Channels: Data.Data_Ch1, Data.Data_Ch2, Data.Data_Ch3, Data.Data_Ch4, Data.Data_Ch5)
            File name required (default path)
        '''
        print('Reading Data')
        with open(name,'r') as fid:
            self.line=''
            while self.line[0:4] != '----':
                self.line = fid.readline()
                print(self.line)
                if self.line[0:2] == 'Fs':
                    self.p, self.q, self.m, self.n = self.line.strip().split(' ')
                    self.Fs = float(self.m)
                    print('Fs = %f\n'%self.Fs)
            self.out_str = fid.readlines()
        self.Data_Ch1, self.Data_Ch2, self.Data_Ch3, self.Data_Ch4, self.Data_Ch5, self.Data_Ch6 = [], [], [], [], [], []
        for self.line in self.out_str:
            self.a, self.b, self.c = self.line.strip().split(', ')
            self.Data_Ch1.append(float(self.a))
            self.Data_Ch2.append(float(self.b))
            self.Data_Ch3.append(float(self.c))
#             self.Data_Ch4.append(float(self.d))    
#             self.Data_Ch5.append(float(self.e))
#             self.Data_Ch6.append(float(self.f))
        
        self.Data_Ch1 = np.array(self.Data_Ch1)
        self.Data_Ch2 = np.array(self.Data_Ch2)
        self.Data_Ch3 = np.array(self.Data_Ch3)
#         self.Data_Ch4 = np.array(self.Data_Ch4)
#         self.Data_Ch5 = np.array(self.Data_Ch5)
#         self.Data_Ch6 = np.array(self.Data_Ch6)
        
        return self.Data_Ch1, self.Data_Ch2, self.Data_Ch3, self.Data_Ch4, self.Data_Ch5, self.Data_Ch6, self.Fs
    
    
    def Read_Data_AlaVar(self, name):
        print('Reading Data')
        with open(name,'r') as fid:
            self.line=''
            while self.line[0:4] != '----':
                self.line = fid.readline()
                print(self.line)
            self.out_str = fid.readlines()
        self.Data_set = []
        for self.line in self.out_str:
            self.a = self.line
            self.Data_set.append(float(self.a))
            
        self.Data_set = np.array(self.Data_set)
        
        return self.Data_set
    
        
    def Export_Data(self, file_name, header, out_str):
        print('Writing Data')
        with open(file_name,'w') as fid: ######################################################################################
            fid.writelines(header)
            fid.writelines(out_str)
        print('Finish Writing')
        return
        
        
    
    def STD(self, Data):
        '''
            Standard Deviation
        '''
        self.Mean_Data = np.mean(Data)
        self.STD_count = []
        for self.i in range(len(Data)):
            self.a = (Data[self.i] - self.Mean_Data) ** 2
            self.STD_count.append(self.a)
        self.Data_STD = (sum(self.STD_count)/(len(Data)-1))**0.5
        return self.Data_STD
        
    def FFT(self, Data, Fs):
        '''
            FFT
        '''
        self.FFT_freqline = np.fft.fftfreq(len(Data), d=1/Fs)[1:len(Data)//2]
        self.Data_FFT = np.abs(np.fft.fft(Data)[1:len(Data)//2])   #two sides FFT
        self.Data_FFT_Volt = self.Data_FFT * 2/len(Data)
    
        return self.FFT_freqline, self.Data_FFT, self.Data_FFT_Volt
    
    def PSD(self, Data, Fs):
        self.FFT(Data, Fs)
        self.PSD_freqline = self.FFT_freqline
        self.PS = (self.Data_FFT ** 2)/len(Data)
        self.PSD = self.PS / Fs
        for self.k in range(1, len(self.PSD)):
            self.PSD[self.k] = self.PSD[self.k] * 2
        
        return self.PSD_freqline, self.PSD
    
    def PSD_Scipy(self, Data, Fs):
        self.Scipy_Freq, self.Scipy_PSD = signal.periodogram(Data, Fs)
        self.Scipy_Freq = self.Scipy_Freq[1:]
        self.Scipy_PSD = self.Scipy_PSD[1:]
        self.Scipy_Noise = np.sqrt(self.Scipy_PSD)
        
        return self.Scipy_Freq, self.Scipy_PSD, self.Scipy_Noise
    
    
    
    
    
    
    
    
    
    