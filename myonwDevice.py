import atoma, requests
import BAC0
import re
from datetime import datetime
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
from BAC0.tasks.RecurringTask import RecurringTask

import time
from BAC0.core.devices.local.models import (
    analog_input,
    datetime_value,
    character_string,
    analog_output,
    binary_output,
    binary_input,
)

print("Starting BACnet device")
new_device = BAC0.lite(deviceId=10031)
time.sleep(1)

# Analog Values
_new_objects = analog_input(
    instance=1,
    name="Current_Temp",
    description="Current Temperature in degC",
    presentValue=0,
    properties={"units": "degreesCelsius"},
)
_new_objects = analog_input(
    instance=2,
    name="Current_Pressure",
    description="Current Pressure in kPa",
    presentValue=0,
    properties={"units": "kilopascals"},
)
# Character Strings
_new_objects = character_string(
    instance=1,
    name="City",
    description="City code for data",
    presentValue="on-24",
    is_commandable=True,
)
# DateTime Values
_new_objects = datetime_value(instance=1, name="Last_Update")

# This line will add all objects to the device
_new_objects.add_objects_to_application(new_device)


while True:
    _new_objects.objects["Last_Update"].presentValue =  DateTime(date=Date().now().value, time=Time().now().value)
    time.sleep(1)
    pass