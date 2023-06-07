from vcgencmd import Vcgencmd
from enum import Enum
from datetime import datetime
import json
import psutil

class Displays(Enum):
    MainLCD = 0
    SecondaryLCD = 1
    HDMI0 = 2
    Composite = 3
    HDMI1 = 7
    
vc = Vcgencmd()

class Mainteance:
    
    def getTemperature(self):
        return vc.measure_temp()

    def getVolts(self):
        return vc.measure_volts('core')
        
    def getClock(self):
        clockData = {}
        clockData.update({'ARM cores' : vc.measure_clock('arm')})
        clockData.update({'VC4 scaler cores' : vc.measure_clock('core')})
        clockData.update({'Image Signal Processor' : vc.measure_clock('isp')})
        clockData.update({'3D block' : vc.measure_clock('v3d')})
        clockData.update({'UART' : vc.measure_clock('uart')})
        clockData.update({'pwm' : vc.measure_clock('pwm')})
        clockData.update({'emmc' : vc.measure_clock('emmc')})
        clockData.update({'Pixel valve' : vc.measure_clock('pixel')})
        clockData.update({'Analogue video encoder' : vc.measure_clock('vec')})
        clockData.update({'HDMI' : vc.measure_clock('hdmi')})
        clockData.update({'Display Peripheral Interface' : vc.measure_clock('dpi')})
        return clockData

    def getDisplay(self):
        data = {}
        data.update({Displays.MainLCD.name : vc.display_power_state(Displays.MainLCD.value)})
        data.update({Displays.SecondaryLCD.name : vc.display_power_state(Displays.SecondaryLCD.value)})
        data.update({Displays.HDMI0.name : vc.display_power_state(Displays.HDMI0.value)})
        data.update({Displays.Composite.name : vc.display_power_state(Displays.Composite.value)})
        data.update({Displays.HDMI1.name : vc.display_power_state(Displays.HDMI1.value)})
        return data
        
    def getCpuUsage(self):
        data = {"Cpu usage" : psutil.cpu_percent()}
        return data

    def getLoadAvg(self):
        data = {"Load average" : psutil.getloadavg()}
        return data
        
    def getVirtualMemory(self):
        data = {"Virtual memory" : psutil.virtual_memory()}
        return data
        
    def getDiskUsage(self):
        data = {"Disk usage" : psutil.disk_usage("/")}
        return data
        
    def getNetworkConnections(self):
        data = {"Network connections" : psutil.net_connections()}
        return data

    def getCurrentUsers(self):
        data = {"Connected users" : psutil.users()}
        return data

    def getDateTime(self):
        data = {"Server time" : datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
        return data
        
    def getFullMainteance(self):
        data = {}
        data.update({"cpu temperature" : self.getTemperature()})
        data.update({"cpu volts" : self.getVolts()})
        data.update({"clocks" : self.getClock()})
        data.update({"displays" : self.getDisplay()})
        data.update({"Cpu usage" : self.getCpuUsage()})
        data.update({"Load average" : self.getLoadAvg()})
        data.update({"Virtual memory" : self.getVirtualMemory()})
        data.update({"Disk usage" : self.getDiskUsage()})
        data.update({"Time" : self.getDateTime()})


        return data
