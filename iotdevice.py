import atoma, requests
import BAC0
import re
from datetime import datetime
import random
from bacpypes.basetypes import EngineeringUnits, DateTime
from bacpypes.primitivedata import CharacterString, Date, Time

from BAC0.core.devices.create_objects import (
    create_AV,
    create_MV,
    create_BV,
    create_AI,
    create_BI,
    create_AO,
    create_BO,
    create_CharStrValue,
    create_DateTimeValue,
)
from BAC0.tasks.RecurringTask import RecurringTask

import time


def start_device():
    print("Starting BACnet device")
    new_device = BAC0.lite(deviceId=10031)
    time.sleep(1)
    # Analog Values
    av = []
    current_temp = create_AV(oid=1, name="Current_Temp", pv=0, pv_writable=False)
    current_temp.units = EngineeringUnits("degreesCelsius")
    current_temp.description = CharacterString("Current Temperature in degC")
    av.append(current_temp)
    current_pressure = create_AV(
        oid=2, name="Current_Pressure", pv=0, pv_writable=False
    )
    current_pressure.units = EngineeringUnits("kilopascals")
    current_pressure.description = CharacterString("Current Pressure in kPa")
    av.append(current_pressure)
    current_dewpoint = create_AV(
        oid=3, name="Current_DewPoint", pv=0, pv_writable=False
    )
    current_dewpoint.units = EngineeringUnits("degreesCelsius")
    current_dewpoint.description = CharacterString("Current Dew Point in degC")
    av.append(current_dewpoint)
    current_humidity = create_AV(
        oid=4, name="Current_Humidity", pv=0, pv_writable=False
    )
    current_humidity.units = EngineeringUnits("percentRelativeHumidity")
    current_humidity.description = CharacterString(
        "Current Humidity in percent relative humidity"
    )
    av.append(current_humidity)
    current_wind_speed = create_AV(
        oid=5, name="Current_Wind_Speed", pv=0, pv_writable=False
    )
    current_wind_speed.units = EngineeringUnits("kilometersPerHour")
    current_wind_speed.description = CharacterString("Current Wind Speed in km/h")
    av.append(current_wind_speed)
    current_visibility = create_AV(
        oid=6, name="Current_Visibility", pv=0, pv_writable=False
    )
    current_visibility.units = EngineeringUnits("kilometers")
    current_visibility.description = CharacterString("Current Visibility in km")
    av.append(current_visibility)

    # CharacterStringValues
    charstr = []
    default_pv = CharacterString("empty")
    location = create_CharStrValue(oid=1, name="Location", pv=default_pv)
    charstr.append(location)
    current_pressure_tend = create_CharStrValue(
        oid=2, name="Current_Press_Tend", pv=default_pv
    )
    charstr.append(current_pressure_tend)
    current_conditions = create_CharStrValue(
        oid=3, name="Current_Conditions", pv=default_pv
    )
    charstr.append(current_conditions)
    current_wind_direction = create_CharStrValue(
        oid=4, name="Current_Wind_Dir", pv=default_pv
    )
    charstr.append(current_wind_direction)

    # DateTimeValueObjects
    dtv = []
    updated = create_DateTimeValue(
        oid=1, name="Current_Conditions_Update", date=None, time=None
    )
    dtv.append(updated)

    for each in av:
        # print(each)
        new_device.this_application.add_object(each)
    for each in charstr:
        new_device.this_application.add_object(each)
    for each in dtv:
        new_device.this_application.add_object(each)
    return new_device


class App:
    dev = start_device()
    # meteo = MeteoGC(city="qc-147", lang="e")


app = App()


def update():
    # print(app.meteo.actual_conditions)
    # app.meteo.update()
    current_temp = app.dev.this_application.get_object_id(("analogValue", 1))
    current_pressure = app.dev.this_application.get_object_id(("analogValue", 2))
    current_dewpoint = app.dev.this_application.get_object_id(("analogValue", 3))
    current_humidity = app.dev.this_application.get_object_id(("analogValue", 4))
    current_wind_speed = app.dev.this_application.get_object_id(("analogValue", 5))
    current_visibility = app.dev.this_application.get_object_id(("analogValue", 6))

    location = app.dev.this_application.get_object_id(("characterstringValue", 1))
    current_pressure_tend = app.dev.this_application.get_object_id(
        ("characterstringValue", 2)
    )
    current_conditions = app.dev.this_application.get_object_id(
        ("characterstringValue", 3)
    )
    current_wind_direction = app.dev.this_application.get_object_id(
        ("characterstringValue", 4)
    )

    updated = app.dev.this_application.get_object_id(("datetimeValue", 1))

    current_temp.presentValue = random.randint(25, 33)
    current_pressure.presentValue = random.randint(25, 33)
    current_dewpoint.presentValue = random.randint(25, 33)
    current_humidity.presentValue = random.randint(25, 33)
    current_wind_speed.presentValue = random.randint(25, 33)
    current_visibility.presentValue = random.randint(25, 33)

    location.presentValue = CharacterString("Armada International")
    current_pressure_tend.presentValue = CharacterString("Steady")
    current_conditions.presentValue = CharacterString("Normal")
    current_wind_direction.presentValue = CharacterString("North")

    updated.presentValue.date = Date(current_dateTime = datetime.now())

    updated.presentValue.time = Time(datetime.now())


def main():
    task_device = RecurringTask(update, delay=300)
    task_device.start()
    task_device.stop()
    while True:
        pass


if __name__ == "__main__":
    main()