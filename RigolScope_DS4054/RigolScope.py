# -*- coding: utf-8 -*-
'''
Created on 07.12.2017

@author: yu03
'''
import visa
import numpy as np
# import time

class RigolScope():
    '''

    '''
    def __init__(self,info):
        '''
            needs the string from Ultra Sigma
        'USB0::0x1AB1::0x04B1::DS4A140800046::INSTR'
        '''
        self.rm = visa.ResourceManager()
        self.dev = self.rm.open_resource(info)
        return
    
#     def Read_ID(self):
#         return self.dev.query('*IDN?')

    def Read_ID(self):
        self.dev.write('*IDN?')
        self.r = self.dev.read()
        return self.r
    
    def Write_AUToscale(self):
        self.dev.write(':AUToscale')
        return
   
    def Write_Run(self):
        self.dev.write(':RUN')
        return
    
    def Write_Stop(self):
        self.dev.write(':STOP')
        return    
    
    def Write_Single(self):
        self.dev.write(':SINGLE')
        return
    
    def Read_WavFormat(self):
        '''
            Queries the return format of the waveform data
        '''
        self.dev.write(':WAVeform:FORMat?')
#         return self.dev.query(':WAVeform:FORMat?')
        return self.dev.read()
    
    def Write_WavFormat_Word(self):
        '''
            Sets the return format of the waveform data to be 'WORD'
        '''
        self.dev.write(':WAVeform:FORMat WORD')
        return    
    
    def Write_WavFormat_Byte(self):
        '''
            Sets the return format of the waveform data to be 'BYTE'
        '''
        self.dev.write(':WAVeform:FORMat BYTE')
        return    
    
    def Write_WavFormat_Ascii(self):
        '''
            Sets the return format of the waveform data to be 'ASCII'
        '''
        self.dev.write(':WAVeform:FORMat ASCii')
#         return

    def Read_WavMode(self):
        '''
            Queries the reading mode of the waveform data
        '''
        return self.dev.query(':WAVeform:MODE?',delay=0.1)
    
    def Write_WavMode_Norm(self):
        '''
            Sets the reading mode of the waveform data to be 'NORMAL'
        '''
        self.dev.write(':WAVeform:MODE NORMal')
        return
    
    def Write_WavMode_Raw(self):
        '''
            Sets the reading mode of the waveform data to be 'RAW'
        '''
        self.dev.write(':WAVeform:MODE RAW')
        return
    
    def Write_WavMode_Max(self):
        '''
            Sets the reading mode of the waveform data to be 'MAXIMUM'
        '''
        self.dev.write(':WAVeform:MODE MAXimum')
        return
    
    def Read_WavPoints(self):
        '''
            Queries the number of the waveform points to be read
        '''
        return self.dev.query(':WAVeform:POINts?',delay=0.1)
    
    def Write_WavPoints(self,Setvalue):
        '''
            Sets the number of the waveform points to be read
            NORMal mode: 1 to 1400
            RAW mode: 1 to the current maximum memory depth
            MAXimum mode: 1 to the number of effective points currently on the screen
        '''
        self.dev.write(':WAVeform:POINts %i'%Setvalue)
        return

    def Read_WavSource(self):
        '''
            Queries the source channel of waveform data reading
        '''
        return self.dev.query(':WAVeform:SOURce?',delay=0.1)
    
    def Write_WavSource_CHAN1(self):
        '''
            Sets the source channel of waveform data reading to be 'CHANNEL 1'
        '''
        self.dev.write('WAVeform:SOURce CHANnel1')
        return
    
    def Write_WavSource_CHAN2(self):
        '''
            Sets the source channel of waveform data reading to be 'CHANNEL 2'
        '''
        self.dev.write('WAVeform:SOURce CHANnel2')
        return
    
    def Write_WavSource_CHAN3(self):
        '''
            Sets the source channel of waveform data reading to be 'CHANNEL 3'
        '''
        self.dev.write('WAVeform:SOURce CHANnel3')
        return
    
    def Write_WavSource_CHAN4(self):
        '''
            Sets the source channel of waveform data reading to be 'CHANNEL 4'
        '''
        self.dev.write('WAVeform:SOURce CHANnel4')
        return
    
    def Write_WavSource_Math(self):
        '''
            Sets the source channel of waveform data reading to be 'MATH'
        '''
        self.dev.write('WAVeform:SOURceMATH')
        return
    
    def Write_WavSource_FFT(self):
        '''
            Sets the source channel of waveform data reading to be 'FFT'
        '''
        self.dev.write('WAVeform:SOURce FFT')
        return
    
    def Read_WavData(self):
        '''
            Queries the waveform data in the buffer
        '''
        return self.dev.query(':WAVeform:DATA?',delay=0.1)
        
    def Read_WavPreSet(self):    
        '''
            Queries the waveform parameter settings related to the waveform data reading
        '''
        return self.dev.query(':WAVeform:PREamble?',delay=0.1)
    
    def Get_WavData_ASC(self):
        '''
            Get Waveform Data Reading (ASCII) into self.Result[] (float)
        '''
        self.DATA = self.Read_WavData()
        
        self.DataLen = self.DATA.count(',')
        self.Result=list(range(self.DataLen))
        self.k = 0
        for self.i in range(self.DataLen):
            if self.DATA[self.k] == '-':
                if self.DATA[self.k+7] == '-':
                    self.Result[self.i] = float(self.DATA[self.k:self.k+11])
                    self.k = self.k+12
                    self.i += 1
#                     print self.Result[1]
                else:
                    self.Result[self.i] = float(self.DATA[self.k:self.k+10])
                    self.k = self.k+11
                    self.i += 1
            else:
                if self.DATA[self.k+6] == '-':
                    self.Result[self.i] = float(self.DATA[self.k:self.k+10])
                    self.k = self.k+11
                    self.i += 1
                else:
                    self.Result[self.i] = float(self.DATA[self.k:self.k+9])
                    self.k = self.k+10
                    self.i += 1
        self.Y_Increment = float(self.Read_Y_Increment())
        self.Y_Origin = float(self.Read_Y_Origin())
        self.Y_Ref = self.Read_Y_Reference()       
        return self.Result

    def Read_Channel_1_Scale(self):
        '''
            Queries the vertical scale of the specified analog channel. 
            The unit is related to the current amplitude unit of the specified analog channel.
            The default unit is V/div.
        '''
        return float(self.dev.query(':CHANnel1:SCALe?',delay=0.1))
    
    def Read_Y_Increment(self):    
        '''
            Queries the unit voltage value of the current source channel (refer to the :WAVeform:SOURce command) in the Y direction. 
            The unit (V) is the same as the current amplitude unit of the source channel. 
            YINCrement=Vertical Scale/32
        '''
        return float(self.dev.query(':WAVeform:YINCrement?',delay=0.1))

    def Read_Y_Origin(self):
        '''
            Queries the vertical position relative to the vertical reference position (refer to the :WAVeform:YREFerence?command)
            of the current source channel (refer to the :WAVeform:SOURce command) in the Y direction.
        '''
        return float(self.dev.query(':WAVeform:YORigin?',delay=0.1))
    
    def Read_Y_Reference(self):
        '''
            Queries the vertical reference position of the current source channel (refer to the :WAVeform:SOURcecommand) in the Y direction.
        '''
        return float(self.dev.query(':WAVeform:YREFerence?',delay=0.1))
    
    def Read_Channel_1_Offset(self):
        '''
            Queries the vertical position of channel_1
        '''
        return float(self.dev.query(':CHANnel1:OFFSet?',delay=0.1))

    def Get_WavData_AllChannel(self):
        '''
            Get Waveform Data Reading (ASCII) for each Channel into self.Result_1-4[] (float)
        '''
        
        self.Write_WavSource_CHAN1()
        self.Result_Ch1 = self.Get_WavData_ASC()
        self.Y_Scale_1 = self.Read_Y_Increment()*32
        self.Y_Origin_1 = self.Read_Y_Origin()
        self.Result_test = self.Result_Ch1
        
        self.Write_WavSource_CHAN2()
        self.Result_Ch2 = self.Get_WavData_ASC()
        self.Y_Scale_2 = self.Read_Y_Increment()*32
        self.Y_Origin_2 = self.Read_Y_Origin()
        
        self.Write_WavSource_CHAN3()
        self.Result_Ch3 = self.Get_WavData_ASC()
        self.Y_Scale_3 = self.Read_Y_Increment()*32
        self.Y_Origin_3 = self.Read_Y_Origin()
        
#         self.Write_WavSource_CHAN4()
#         self.Result_Ch4 = self.Get_WavData_ASC()
#         self.Y_Scale_4 = self.Read_Y_Increment()*32
#         self.Y_Origin_4 = self.Read_Y_Origin()
        
# #         self.Result_Ch1 = [(x+self.Y_Scale_2*(self.Y_Origin_2/self.Y_Scale_2-self.Y_Origin_1/self.Y_Scale_1))  for x in self.Result_Ch1]
#         self.Result_Ch1 = [(x)  for x in self.Result_Ch1]
#         self.Result_Ch2 = [(x)  for x in self.Result_Ch2]
#         self.Result_Ch3 = [(x+self.Y_Scale_4*(self.Y_Origin_4/self.Y_Scale_4-self.Y_Origin_3/self.Y_Scale_3))  for x in self.Result_Ch3]
#         self.Result_Ch4 = [(x+self.Y_Scale_1*(self.Y_Origin_1/self.Y_Scale_1-self.Y_Origin_4/self.Y_Scale_4))  for x in self.Result_Ch4]
        
        return self.Result_Ch1, self.Result_Ch2, self.Result_Ch3

    def Read_X_Increment(self):
        '''
            Queries the time difference (the default unit is s) between two neighboring points
            of the current source channel in the X direction
            XINCrement = TimeScale/100
            !!!Wrong Return!!!
        '''
        return float(self.dev.query(':WAVeform:XINCrement?',delay=0.1))

    def Read_Sample_Rate(self):
        '''
            Queries the current sample rate of the oscilloscope. The default unit is Sa/s.
        '''
        return float(self.dev.query(':ACQuire:SRATe?',delay=0.1))

    def Read_Memory_Depth(self):
        '''
            Queries the current sample rate of the oscilloscope. The default unit is Sa/s.
        '''
        return int(self.dev.query(':ACQuire:MDEPth?',delay=0.1))
    
    def Write_WavReading_Reset(self):
        '''
            Resets the waveform data reading.
            This command is only applicable to reading waveform data in the internal memory 
        '''
        self.dev.write(':WAVeform:RESet')
        return
    
    def Write_WavReading_Begin(self):
        '''
            Starts the waveform data reading.
            This command is only applicable to reading waveform data in the internal memory 
        '''
        self.dev.write(':WAVeform:BEGin')
        return
    
    def Read_WavReading_Status(self):
        '''
            Queries the current status of waveform data reading.
            IDLE,<n>: indicates that the waveform data reading thread finishes; <n> is the number of waveform points that have been read.
            READ,<n>: indicates that the waveform data reading thread is running; <n> is the number of waveform points that have currently been read
        '''
        return self.dev.query(':WAVeform:STATus?',delay=0.1)
    
    def Write_WavReading_End(self):
        '''
            Stops the waveform data reading.
            This command is only applicable to reading waveform data in the internal memory 
        '''
        self.dev.write(':WAVeform:END')
        return
    
    def Get_Buffer_Ch1(self):
        '''
            Queries waveform data (and points number) of Channel 1 from the internal memory 
        '''
        self.Write_Stop()
         
        self.Scale_1 = float(self.dev.query(':CHANnel1:SCALe?'))
#         print self.Scale_1
        self.Offset_1 = float(self.dev.query(':CHANnel1:OFFSet?'))
        self.Scale_2 = float(self.dev.query(':CHANnel2:SCALe?'))
        self.Offset_2 = float(self.dev.query(':CHANnel2:OFFSet?'))
        self.dev.write(':CHANnel1:SCALe %f'%self.Scale_1)
  
        self.Write_WavSource_CHAN1()
        self.Write_WavMode_Raw()
        self.MemDep = self.Read_Memory_Depth()
        self.Write_WavPoints(self.MemDep)
#         self.Write_WavPoints(100)
        self.Write_WavReading_Reset()
        self.Write_WavReading_Begin()
        self.BufData_Ch1 = list()
        self.BufLen_Ch1 = 0
        self.count = 0
         
        status,remain_cnt = self.Read_WavReading_Status().split(',')
         
#         while status[0:4]!='READ':
        while remain_cnt[0] == '0':
            status,remain_cnt = self.Read_WavReading_Status().split(',')
        print ('CHANNEL_1 start reading')
        while status[0:4] == 'READ':
            tmp = [float(i) for i in self.Read_WavData().strip().split(',')[:-1]]
            self.BufData_Ch1 = self.BufData_Ch1 + tmp
            self.count += 1
            print (self.count)
            status,remain_cnt = self.Read_WavReading_Status().split(',')
             
        if (int(remain_cnt)>0):
            tmp = [float(i) for i in self.Read_WavData().strip().split(',')[:-1]]
            self.BufData_Ch1 = self.BufData_Ch1 + tmp
            self.count += 1
            print (self.count)
         
        if status!='IDLE':
            print ('Unexpected status %s'%status)
         
        self.Write_WavReading_End()
        self.BufData_Ch1_RealV = [(x + self.Offset_2)/self.Scale_2*self.Scale_1 - self.Offset_1 for x in self.BufData_Ch1] #####Function from test, differ from expected
        print ('finish reading')    
        print ('Data Size:', len(self.BufData_Ch1))
        return self.BufData_Ch1_RealV

    def Get_Buffer_Ch2(self):
        '''
            Queries waveform data (and points number) of Channel 2 from the internal memory 
        '''
        self.Write_Stop()
        
        self.Scale_2 = float(self.dev.query(':CHANnel2:SCALe?'))
        self.Offset_2 = float(self.dev.query(':CHANnel2:OFFSet?'))
        self.Scale_3 = float(self.dev.query(':CHANnel3:SCALe?'))
        self.Offset_3 = float(self.dev.query(':CHANnel3:OFFSet?'))
        self.dev.write(':CHANnel2:SCALe %f'%self.Scale_2)

        self.Write_WavSource_CHAN2()
        self.Write_WavMode_Raw()
        self.MemDep = self.Read_Memory_Depth()
        self.Write_WavPoints(self.MemDep)
#         self.Write_WavPoints(100)
        self.Write_WavReading_Reset()
        self.Write_WavReading_Begin()
        
        self.BufData_Ch2 = list()
        self.BufLen_Ch2 = 0
        self.count = 0
        
        status,remain_cnt = self.Read_WavReading_Status().split(',')
        
#         while status[0:4]!='READ':
        while remain_cnt[0] == '0':
            status,remain_cnt = self.Read_WavReading_Status().split(',')
            
        print ('CHANNEL_2 start reading')
        
        while status[0:4] == 'READ':
            tmp = [float(i) for i in self.Read_WavData().strip().split(',')[:-1]]
            self.BufData_Ch2 = self.BufData_Ch2 + tmp
            self.count += 1
            print (self.count)
            status,remain_cnt = self.Read_WavReading_Status().split(',')
            
        if (int(remain_cnt)>0):
            tmp = [float(i) for i in self.Read_WavData().strip().split(',')[:-1]]
            self.BufData_Ch2 = self.BufData_Ch2 + tmp
            self.count += 1
            print (self.count)
        
        if status!='IDLE':
            print ('Unexpected status %s'%status)
            
        self.Write_WavReading_End()
        self.BufData_Ch2_RealV = [(x + self.Offset_3)/self.Scale_3*self.Scale_2 - self.Offset_2 for x in self.BufData_Ch2] #####Function from test, differ from expected
        print ('finish reading')    
        print ('Data Size:', len(self.BufData_Ch2))
        return self.BufData_Ch2_RealV



#     def Get_Buffer_Ch2(self):
#         '''
#             Queries waveform data (and points number) of Channel 2 from the internal memory 
#         '''
#         self.Write_Stop()
#         self.Write_WavSource_CHAN2()
#         self.Write_WavMode_Raw()
#         self.MemDep = self.Read_Memory_Depth()
#         self.Write_WavPoints(self.MemDep)
# #         self.Write_WavPoints(100)
#         self.Write_WavReading_Reset()
#         self.Write_WavReading_Begin()
#         time.sleep(2)
#         self.BufData_Ch2 = list()
#         self.BufLen_Ch2 = 0
#         self.count = 0
#         while self.Read_WavReading_Status()[0:4] == 'READ':
# #             time.sleep(0.1)
#             self.BufData_Ch2 = self.BufData_Ch2 + self.Get_WavData_ASC()
#             self.BufLen_Ch2 = self.BufLen_Ch2 + self.DataLen
#             self.count += 1
# #             time.sleep(1)
#             print self.count
#         else:
# #             time.sleep(0.1)
#             self.BufData_Ch2 = self.BufData_Ch2 + self.Get_WavData_ASC()
#             self.BufLen_Ch2 = self.BufLen_Ch2 + self.DataLen
#             self.count += 1
#             print self.count
#         print self.Read_WavReading_Status()
#         self.Write_WavReading_End()
#         return self.BufData_Ch2, self.BufLen_Ch2      
    
    def Get_Buffer_Ch3(self):
        '''
            Queries waveform data (and points number) of Channel 3 from the internal memory 
        '''
        self.Write_Stop()
        
        self.Scale_3 = float(self.dev.query(':CHANnel3:SCALe?'))
        self.Offset_3 = float(self.dev.query(':CHANnel3:OFFSet?'))
        self.Scale_4 = float(self.dev.query(':CHANnel4:SCALe?'))
        self.Offset_4 = float(self.dev.query(':CHANnel4:OFFSet?'))
        self.dev.write(':CHANnel3:SCALe %f'%self.Scale_3)
        
        self.Write_WavSource_CHAN3()
        self.Write_WavMode_Raw()
        self.MemDep = self.Read_Memory_Depth()
        self.Write_WavPoints(self.MemDep)
#         self.Write_WavPoints(100)
        self.Write_WavReading_Reset()
        self.Write_WavReading_Begin()
#         time.sleep(2)
        self.BufData_Ch3 = list()
        self.BufLen_Ch3 = 0
        self.count = 0
        
        status,remain_cnt = self.Read_WavReading_Status().split(',')
        
#         while status[0:4]!='READ':
        while remain_cnt[0] == '0':
            status,remain_cnt = self.Read_WavReading_Status().split(',')
        print ('CHANNEL_3 start reading')
        while status[0:4] == 'READ':
            tmp = [float(i) for i in self.Read_WavData().strip().split(',')[:-1]]
            self.BufData_Ch3 = self.BufData_Ch3 + tmp
            self.count += 1
            print (self.count)
            status,remain_cnt = self.Read_WavReading_Status().split(',')
            
        if (int(remain_cnt)>0):
            tmp = [float(i) for i in self.Read_WavData().strip().split(',')[:-1]]
            self.BufData_Ch3 = self.BufData_Ch3 + tmp
            self.count += 1
            print (self.count)
        
        if status!='IDLE':
            print ('Unexpected status %s'%status)
            
        self.Write_WavReading_End()
        self.BufData_Ch3_RealV = [((x+self.Offset_4)/self.Scale_4)*self.Scale_3-self.Offset_3 for x in self.BufData_Ch3]#####Function from test, differ from expected
        print ('finish reading')  
        print ('Data Size:', len(self.BufData_Ch3))
        return self.BufData_Ch3_RealV
    
    def Get_Buffer_Ch4(self):
        '''
            Queries waveform data (and points number) of Channel 4 from the internal memory 
        '''
        self.Write_Stop()
        
        self.Scale_4 = float(self.dev.query(':CHANnel4:SCALe?'))
        self.Offset_4 = float(self.dev.query(':CHANnel4:OFFSet?'))
        self.Scale_1 = float(self.dev.query(':CHANnel1:SCALe?'))
        self.Offset_1 = float(self.dev.query(':CHANnel1:OFFSet?'))
        self.dev.write(':CHANnel4:SCALe %f'%self.Scale_4)
        
        self.Write_WavSource_CHAN4()
        self.Write_WavMode_Raw()
        self.MemDep = self.Read_Memory_Depth()
        self.Write_WavPoints(self.MemDep)
#         self.Write_WavPoints(100)
        self.Write_WavReading_Reset()
        self.Write_WavReading_Begin()
#         time.sleep(2)
        self.BufData_Ch4 = list()
        self.BufLen_Ch4 = 0
        self.count = 0
        
        status,remain_cnt = self.Read_WavReading_Status().split(',')
        
#         while status[0:4]!='READ':
        while remain_cnt[0] == '0':
            status,remain_cnt = self.Read_WavReading_Status().split(',')
        print ('CHANNEL_4 start reading')
        while status[0:4] == 'READ':
            tmp = [float(i) for i in self.Read_WavData().strip().split(',')[:-1]]
            self.BufData_Ch4 = self.BufData_Ch4 + tmp
            self.count += 1
            print (self.count)
            status,remain_cnt = self.Read_WavReading_Status().split(',')
            
        if (int(remain_cnt)>0):
            tmp = [float(i) for i in self.Read_WavData().strip().split(',')[:-1]]
            self.BufData_Ch4 = self.BufData_Ch4 + tmp
            self.count += 1
            print (self.count)
        
        if status!='IDLE':
            print ('Unexpected status %s'%status)
            
        self.Write_WavReading_End()
        self.BufData_Ch4_RealV = [((x+self.Offset_1)/self.Scale_1)*self.Scale_4-self.Offset_4 for x in self.BufData_Ch4]#####Function from test, differ from expected
        print ('finish reading')   
        print ('Data Size:', len(self.BufData_Ch4))
        return self.BufData_Ch4_RealV
    
    def Read(self):
        '''
            scope.Read_Ch1, scope.Read_Ch2, scope.Read_Ch3, scope.Read_Ch4
        '''
        print(self.Read_ID())
        self.Write_WavFormat_Ascii()
        print('Start Reading')
        self.Read_Ch1 = np.array(self.Get_Buffer_Ch1())
        self.Read_Ch2 = np.array(self.Get_Buffer_Ch2())
#         self.Read_Ch3 = np.array(self.Get_Buffer_Ch3())
#         self.Read_Ch4 = np.array(self.Get_Buffer_Ch4())
        self.Memory_Depth = self.Read_Memory_Depth()
        self.Sample_Rate = self.Read_Sample_Rate()
        print('Finish Reading')
        return self.Read_Ch1, self.Read_Ch2, self.Memory_Depth, self.Sample_Rate
#         return self.Read_Ch1, self.Read_Ch2, self.Read_Ch3, self.Read_Ch4, self.Memory_Depth, self.Sample_Rate

    
    
    
    