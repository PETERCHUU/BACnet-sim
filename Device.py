
import BAC0
import random
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
import time
from BAC0.core.devices.local.models import (
    analog_input,
    datetime_value,
    character_string,
    analog_output,
    binary_output,
    binary_input,
)



tempStart=16.0
tempEnd=30.0
PressureStart=101.9
PressureEnd=102.1
FireAlarm=False


print("Starting BACnet device")
new_device = BAC0.lite(deviceId=10031)
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


while True:
    _new_objects.objects["Last_Update"].presentValue =  DateTime(date=Date().now(), time=Time().now())
    _new_objects.objects["Current_Temp"].presentValue = round(random.uniform(tempStart, tempEnd), 2)
    _new_objects.objects["Current_Pressure"].presentValue = round(random.uniform(PressureStart, PressureEnd), 2)
    time.sleep(1)
    pass




# BACDevice = threading.Thread(target=StartBACDevice,args=(queuer,1))
# BACDevice.start()
# userInput=threading.Thread(target=userUpdate,args=(queuer,1))
# userInput.start()

StartBACDevice()