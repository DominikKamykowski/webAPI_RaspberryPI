from vcgencmd import Vcgencmd
from enum import Enum
import json

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
        return vc.measure_clock('arm')

    def getDisplay(self):
        json = {}
        json.update({Displays.MainLCD.name : vc.display_power_state(Displays.MainLCD.value)})
        json.update({Displays.SecondaryLCD.name : vc.display_power_state(Displays.SecondaryLCD.value)})
        json.update({Displays.HDMI0.name : vc.display_power_state(Displays.HDMI0.value)})
        json.update({Displays.Composite.name : vc.display_power_state(Displays.Composite.value)})
        json.update({Displays.HDMI1.name : vc.display_power_state(Displays.HDMI1.value)})
        return json
