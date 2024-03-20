
import BAC0
import random
import signal
import queue
from BAC0.core.devices.local.object import ObjectFactory
from bacpypes.basetypes import EngineeringUnits, DateTime
from bacpypes.primitivedata import CharacterString, Date, Time
from bacpypes.object import (
    AnalogInputObject,
    AnalogOutputObject,
    AnalogValueObject,
    BinaryInputObject,
    BinaryValueObject,
    CharacterStringValueObject,
    DateTimeValueObject,
    MultiStateValueObject,
)
from Ticker import Ticker
from BAC0.tasks.RecurringTask import RecurringTask
import threading
import time
from BAC0.core.devices.local.models import (
    analog_input,
    datetime_value,
    character_string,
    analog_output,
    binary_output,
    binary_input,
)
import sys
class settingObject:
    def __init__(self,tempStart,tempEnd,pressureStart,PressureEnd,fireAlarm) -> None:
        self.tempStart = tempStart
        self.tempEnd = tempEnd
        self.PressureStart = pressureStart
        self.PressureEnd = PressureEnd
        self.FireAlarm = fireAlarm
        pass
TIMEOUT = 120 # number of seconds your want for timeout

def interrupted(signum, frame):
    "called when read times out"
    print('interrupted!')



queuer = queue.Queue()



def StartBACDevice(queue:queue.Queue):
    print("Starting BACnet device")
    setting=settingObject(16.0,30.0,101.9,102.1,False)
    new_device = BAC0.lite(deviceId=10031)
    time.sleep(1)
    
    # Analog Values
    _new_objects = analog_input(
        instance=1,
        name="Current_Temp",
        description="Current Temperature in degC",
        presentValue=round(random.uniform(setting.tempEnd, setting.tempEnd), 2),
        properties={"units": "degreesCelsius"},
    )
    analog_input(
        instance=2,
        name="Current_Pressure",
        description="Current Pressure in kPa",
        presentValue=round(random.uniform(setting.PressureStart, setting.PressureEnd), 2),
        properties={"units": "kilopascals"},
    )
    binary_input(
        instance=1,
        name="Fire_Alarm",
        description="Server room fire alarm",
        presentValue=setting.FireAlarm,
    )
    character_string(
        instance=1,
        name="Room",
        description="City code for data",
        presentValue="Armada server Room",
        is_commandable=True,
    )
    datetime_value(instance=1, name="Last_Update")

    # This line will add all objects to the device
    _new_objects.add_objects_to_application(new_device)


    while True:
        if queue.not_empty:
            settingQ=settingObject(queue.get())
            if settingQ.FireAlarm!=None:
                _new_objects.objects["Fire_Alarm"].presentValue = settingQ.FireAlarm
            if settingQ.tempStart!=None:
                setting.tempStart=settingQ.tempStart
            if settingQ.tempEnd!=None:
                setting.tempEnd=settingQ.tempEnd
            if settingQ.PressureStart!=None:
                setting.PressureStart=settingQ.PressureStart
            if settingQ.PressureEnd!=None:
                setting.PressureEnd=settingQ.PressureEnd
        _new_objects.objects["Last_Update"].presentValue =  DateTime(date=Date().now().value, time=Time().now().value)
        _new_objects.objects["Current_Temp"].presentValue = round(random.uniform(setting.tempStart, setting.tempEnd), 2)
        _new_objects.objects["Current_Pressure"].presentValue = round(random.uniform(setting.PressureStart, setting.PressureEnd), 2)
        time.sleep(1)
        pass

def userUpdate(queue:queue.Queue):
    while True:
        password=input("Press Enter Password to change setting")
        if password=="P@ssw0rd":
            setting=settingObject()
            timer=Ticker(30)
            timer.start()
            try:
                print("please select the setting you want to change")
                print("1. Temperature Range")
                print("2. Pressure Range")
                print("3. Fire Alarm")
                print("4. Exit")
                print("Enter your choice: ")
                while t.evt.wait():
                    choice = sys.stdin.readline().strip()
                    if choice == "1":
                        try:
                            print("Enter the start temperature: ")
                            setting.tempStart = float(sys.stdin.readline().strip())
                            print("Enter the end temperature: ")
                            setting.tempEnd = float(sys.stdin.readline().strip())
                            queue.put(setting)
                        except:
                            print("Invalid Input")
                    elif choice == "2":
                        print("Enter the start pressure: ")
                        setting.PressureStart = float(sys.stdin.readline().strip())
                        print("Enter the end pressure: ")
                        setting.PressureEnd = float(sys.stdin.readline().strip())
                        queue.put(setting)
                    elif choice == "3":
                        print("Enter the fire alarm status: ")
                        print("1. True, other is False")
                        number=int(sys.stdin.readline().strip())
                        setting.FireAlarm = True if number==1 else False
                        queue.put(setting)
                    else:
                        break
            except:
                timer.stop()
                timer.join()
                print("input Timeout")
        time.sleep(1)


BACDevice = threading.Thread(StartBACDevice,args=(queuer,1))
BACDevice.start()
userUpdate(queuer)