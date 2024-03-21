import random
import Ticker
import threading,time,sys,queue
import BAC0
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
from BAC0.core.devices.local.models import (
    analog_input,
    datetime_value,
    character_string,
    analog_output,
    binary_output,
    binary_input,
)




def StartBACDevice():
    print("Starting BACnet device")
    new_device = BAC0.lite(deviceId=100)
    time.sleep(1)

    # Analog Values
    _new_objects = analog_input(
        instance=1,
        name="Current_Temp",
        description="Current Temperature in degC",
        presentValue=round(random.uniform(tempEnd, tempEnd), 2),
        properties={"units": "degreesCelsius"},
    )
    analog_input(
        instance=2,
        name="Current_Pressure",
        description="Current Pressure in kPa",
        presentValue=round(random.uniform(PressureStart, PressureEnd), 2),
        properties={"units": "kilopascals"},
    )
    binary_input(
        instance=1,
        name="Fire_Alarm",
        description="Server room fire alarm",
        presentValue=FireAlarm,
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


    # while True:
    #     _new_objects.objects["Last_Update"].presentValue =  DateTime(date=Date().now(), time=Time().now())
    #     _new_objects.objects["Current_Temp"].presentValue = round(random.uniform(tempStart, tempEnd), 2)
    #     _new_objects.objects["Current_Pressure"].presentValue = round(random.uniform(PressureStart, PressureEnd), 2)
    #     time.sleep(1)
    #     pass
    return new_device




# BACDevice = threading.Thread(target=StartBACDevice,args=(queuer,1))
# BACDevice.start()
# userInput=threading.Thread(target=userUpdate,args=(queuer,1))
# userInput.start()


queuer = queue.Queue()
tempStart=16.0
tempEnd=30.0
PressureStart=101.9
PressureEnd=102.1
FireAlarm=False
class settingObject:
    def __init__(self,tempStart,tempEnd,pressureStart,PressureEnd,fireAlarm) -> None:
        self.tempStart = tempStart
        self.tempEnd = tempEnd
        self.PressureStart = pressureStart
        self.PressureEnd = PressureEnd
        self.FireAlarm = fireAlarm
        pass
    def placeSetting(self,Setting):
        if Setting.tempStart:
            self.tempStart=Setting.tempStart
        if Setting.tempEnd:
            self.tempEnd=Setting.tempEnd
        if Setting.PressureStart:
            self.PressureStart=Setting.PressureStart
        if Setting.PressureEnd:
            self.PressureEnd=Setting.PressureEnd
        if Setting.FireAlarm:
            self.FireAlarm=Setting.FireAlarm
DefaultSetting=settingObject(tempStart,tempEnd,PressureStart,PressureEnd,FireAlarm)

bacDevice=StartBACDevice()
# bacDevice.modelName = "BACnet Device"
# bacDevice.description = "BACnet Device"
# bacDevice.location = "BACnet Device"
# bacDevice.vendorName = "BACnet Device"
# bacDevice.vendorId=1
# bacDevice.vendorName="BACnet Device"


mainThread = threading.current_thread()
    
def updateDevice(setting:settingObject,queue:queue.Queue):
    while True:
        if not queue.empty():
            q=queue.get()
            setting.placeSetting(q)
            print("Setting Should Update")
        bacDevice.local_objects["Last_Update"].presentValue =  DateTime(date=Date().now(), time=Time().now())
        bacDevice.local_objects["Current_Temp"].presentValue = round(random.uniform(setting.tempStart, setting.tempEnd), 2)
        bacDevice.local_objects["Current_Pressure"].presentValue = round(random.uniform(setting.PressureStart, setting.PressureEnd), 2)
        if not mainThread.is_alive():
            break
        time.sleep(1)
        pass


# class threadTimer:
#     def __init__(self,evt:threading.Thread,time:int) -> None:
#         super().__init__()
#         self.evt=evt
#         self.time=time
#         pass
#     def start(self):
#         time.sleep(self.time)


threading.Thread(target=updateDevice,args=(DefaultSetting,queuer)).start()
while True:
    password=input("Press Enter Password to change setting")
    if password=="P@ssw0rd":
        setting=settingObject(None,None,None,None,None)
        timer=Ticker.Ticker(10)
        try:
            timer.start()
            print("please select the setting you want to change")
            print("1. Temperature Range")
            print("2. Pressure Range")
            print("3. Fire Alarm")
            print("4. Exit")
            print("Enter your choice: ")
            while timer.evt.wait():
                choice = sys.stdin.readline().strip()
                if choice == "1":
                    try:
                        print("Enter the start temperature: ")
                        setting.tempStart =float(sys.stdin.readline().strip())
                        print("Enter the end temperature: ")
                        setting.tempEnd = float(sys.stdin.readline().strip())
                        queuer.put(setting)
                    except:
                        print("Invalid Input")
                elif choice == "2":
                    print("Enter the start pressure: ")
                    setting.PressureStart = float(sys.stdin.readline().strip())
                    print("Enter the end pressure: ")
                    setting.PressureEnd = float(sys.stdin.readline().strip())
                    queuer.put(setting)
                elif choice == "3":
                    print("Enter the fire alarm status: ")
                    print("1. True, other is False")
                    number=int(sys.stdin.readline().strip())
                    setting.FireAlarm = True if number==1 else False
                    queuer.put(setting)
                else:
                    break
        except:
            timer.stop()
            timer.join()
            print("input Timeout")
    pass

