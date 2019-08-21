'''
Created on 28.11.2017

@author: yu03
'''

from NKTP_DLL import *


class NKTLaser():
    '''
     
    '''
    def __init__(self,port):
        '''
            needs the Port string
        laser = NKTLaser.NKTLaser('COM8')
        '''
        self.port = port
    
    def Read_UserArea(self):
        '''
            Return User Area
            BASIK
        '''
        return registerReadAscii(self.port, 1, 0x8D, -1)[1]

    def Read_ModSerNum(self):
        '''
            Return Module Serial Number
            17220227
        '''
        return deviceGetModuleSerialNumberStr(self.port, 1)[1]
    
    def Read_Std_WavLength(self):
        '''
            Return Standard Wavelength in nm
            1550.12
        '''
        return 0.0001*registerReadS32(self.port, 1, 0x32,-1)[1]
        
    def Read_Laser_Emission(self):
        '''
            Returns Laser Emission Checking 
            1=ON; 0=OFF    
        '''
        return registerReadU8(self.port, 1, 0x30, -1)[1]
           
    def Set_Laser_ON(self):
        '''
            Turn On Laser Emission    
        '''
        registerWriteU8(self.port, 1, 0x30, 0x01, -1)

    def Set_Laser_OFF(self):
        '''
            Turn On Laser Emission    
        '''
        registerWriteU8(self.port, 1, 0x30, 0x00, -1)
       
    def Read_Power_mW(self):
        '''
            Returns Power Configuration in mW
        '''
        return 0.01*registerReadU16(self.port, 1, 0x22,-1)[1]    
    
    def Set_Power(self,Power_mW):
        '''
            Set Power Configuration in mW    
        '''
        Power_mW = int(Power_mW * 100)
        registerWriteU16(self.port, 1, 0x22, Power_mW, -1)
        return
    
    def Get_Power_mW(self):
        '''
            Returns Power Monitor in mW
        '''
        return 0.01*registerReadU16(self.port, 1, 0x17,-1)[1]
    
    def Get_Power_dBm(self):
        '''
            Returns Power Monitor in dBm
        '''   
        return 0.01*registerReadU16(self.port, 1, 0x90,-1)[1]
    
    def Get_Temp_deg(self):
        '''
            Returns Temperature Monitor in degree
        '''
        return 0.1 * registerReadS16(self.port, 1, 0x1C,-1)[1]
    
    def Get_Volt_V(self):
        '''
            Returns Voltage Monitor in V
        '''
        return 0.001 * registerReadU16(self.port, 1, 0x1E,-1)[1]
    
    def Read_WavLength_Offset_pm(self):
        '''
            Returns Wavelength Offset Configuration in pm
        '''
        return 0.1 * registerReadS16(self.port, 1, 0x2A,-1)[1]
    
    def Set_WavLength_Offset_pm(self,WavOffset_pm):
        '''
            Set Wavelength Offset in pm 
            -500.0~750.0
        '''
        GivenValue = int(10*WavOffset_pm)
        registerWriteS16(self.port, 1, 0x2A, GivenValue, -1)
        return
    
    def Get_WavLength_Offset_pm(self):
        '''
            Returns Wavelength Offset Monitor in pm
        '''
        return 0.1 *registerReadS16(self.port, 1, 0x72,-1)[1]
        
    def Read_Mod_Source(self):
        '''
            Returns Modulation Source
            4=External; 16=Internal; 20=Both
        '''
        return registerReadU16(self.port, 1, 0x31,-1)[1] & 20
    
    def Set_Mod_Source_Ext(self):
        '''
            Set Modulation Source to be "External"
        '''
        SetValue = 4 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 235)
        registerWriteU16(self.port, 1, 0x31, SetValue, -1)
        return

    def Set_Mod_Source_Int(self):
        '''
            Set Modulation Source to be "Internal"
        '''
        SetValue = 16 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 235)
        registerWriteU16(self.port, 1, 0x31, SetValue, -1)
        return

    def Set_Mod_Source_Both(self):
        '''
            Set Modulation Source to be "Both: External & Internal"
        '''
        SetValue = 20 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 235)
        registerWriteU16(self.port, 1, 0x31, SetValue, -1)
        return
    
    def Read_Mod_Couple(self):
        '''
            Returns Modulation Coupling
            0=AC; 1=DC
        '''
        return (registerReadU16(self.port, 1, 0x31,-1)[1] & 8) / 8
    
    def Set_Mod_Couple_AC(self):
        '''
            Set Modulation Coupling to be AC
        '''
        SetValue = 8 * 0 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 247) 
        registerWriteU16(self.port, 1, 0x31, SetValue, -1)
    
    def Set_Mod_Couple_DC(self):
        '''
            Set Modulation Coupling to be DCs
        '''
        SetValue = 8 * 1 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 247) 
        registerWriteU16(self.port, 1, 0x31, SetValue, -1)

    def Read_DDS_Waveform(self):
        '''
            Returns DDS Waveform (only for Internal Mondulation)
            0=Sinusoidal; 1=Triangle
        '''
        return (registerReadU8(self.port, 1, 0xB7,-1)[1] & 192) / 64        
  
    def Set_DDS_Waveform_SIN(self):
        '''
            Set DDS Waveform to be "Sine" (only for Internal Mondulation)
        '''
        SetValue = 64 * 0 | (registerReadU8(self.port, 1, 0xB7,-1)[1] & 63)
        registerWriteU8(self.port, 1, 0xB7, SetValue, -1)
        return
    
    def Set_DDS_Waveform_TRI(self):
        '''
            Set DDS Waveform to be "Triangle" (only for Internal Mondulation)
        '''
        SetValue = 64 * 1 | (registerReadU8(self.port, 1, 0xB7,-1)[1] & 63)
        registerWriteU8(self.port, 1, 0xB7, SetValue, -1)
        return
    
    def Read_DDS_Emission(self):
        '''
            Returns DDS Output Checking (only for Internal Mondulation)
            0=Disabled(OFF); 1=Enabled(ON)
        '''
        return (registerReadU16(self.port, 1, 0x31,-1)[1] & 32) / 32
    
    def Set_DDS_ON(self):
        '''
            Turn ON DDS Output (only for Internal Mondulation)
        '''
        SetValue = 32 * 1 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 223)
        registerWriteU16(self.port, 1, 0x31, SetValue, -1)
        return
        
    def Set_DDS_OFF(self):
        '''
            Turn OFF DDS Output (only for Internal Mondulation)
        '''
        SetValue = 32 * 0 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 223)
        registerWriteU16(self.port, 1, 0x31, SetValue, -1)
        return
    
    def Read_Mod_Output(self):
        '''
            Returns Modulation Output Checking
            0=OFF; 1=ON
        '''
        return registerReadU8(self.port, 1, 0xB5,-1)[1]
    
    def Set_Mod_Output_ON(self):
        '''
            Turn ON Modulation Output
        '''
        registerWriteU8(self.port, 1, 0xB5, 1, -1)
        return
    
    def Set_Mod_Output_OFF(self):
        '''
            Turn OFF Modulation Output
        '''
        registerWriteU8(self.port, 0, 0xB5, 0, -1)
        return
    
    def Read_Mod_Range(self):
        '''
            Return Modulation Range
            0=Wide; 1=Narrow
        '''
        return (registerReadU16(self.port, 1, 0x31,-1)[1] & 2) / 2
    
    def Set_Mod_Range_Wide(self):
        '''
            Set Modulation Range to be "Wide"
        '''
        SetValue = 2 * 0 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 253)
        registerWriteU16(self.port, 1, 0x31, SetValue,-1)
        return
    
    def Set_Mod_Range_Narrow(self):
        '''
            Set Modulation Range to be "Narrow"
        '''
        SetValue = 2 * 1 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 253)
        registerWriteU16(self.port, 1, 0x31, SetValue,-1)
        return
    
    def Read_PhaCom(self):
        '''
            Return Modulation Phase-Compensation Checking (Only for Narrow Range)
            0=OFF; 1=ON
        '''
        return registerReadU16(self.port, 1, 0x31,-1)[1] & 1
    
    def Set_PhaCom_ON(self):
        '''
            Turn ON Modulation Phase-Compensation (Only for Narrow Range)
        '''
        SetValue = 1 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 254)
        registerWriteU16(self.port, 1, 0x31, SetValue,-1)
    
    def Set_PhaCom_OFF(self):
        '''
            Turn OFF Modulation Phase-Compensation (Only for Narrow Range)
        '''
        SetValue = 0 | (registerReadU16(self.port, 1, 0x31,-1)[1] & 254)
        registerWriteU16(self.port, 1, 0x31, SetValue,-1)
    
    def Read_Mod_Freq_Hz(self):
        '''
            Return Modulation Frequency Configuration in Hz (only for Internal Mondulation)
        '''
        return registerReadF32(self.port, 1, 0xB8,-1)[1]
    
    def Set_Mod_Freq_Hz(self, SetValue):
        '''
            Set Modulation Frequency in Hz (only for Internal Mondulation)
            0.008~100000.000
        '''
        registerWriteF32(self.port, 1, 0xB8, SetValue, -1)
        return
    
    def Read_Mod_Scale(self):
        '''
            Return Modulation Scale Configuration in Hz (only for Internal Mondulation)
        '''
        return 0.001 * registerReadU16(self.port, 1, 0x2B,-1)[1]
    
    def Set_Mod_Scale(self, SetValue):
        '''
            Set Modulation Scale (only for Internal Mondulation)
            0.000~1.000
        '''
        SetValue = int(SetValue*1000)
        registerWriteU16(self.port, 1, 0x2B, SetValue,-1)
        return
    
    
    
    
    
    
    
    
    
    