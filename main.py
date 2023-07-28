from fastapi import FastAPI
from Mainteance import Mainteance
import threading
import time
import board
import busio
import adafruit_gps
from adafruit_bme280 import basic as adafruit_bme280

import serial



app = FastAPI()
mainteance = Mainteance()
sensor_value = None
GPS_value = None
Error_message = {"Error message": "Błąd pobrania danych z systemu"}

def read_GPS():
	global GPS_value
	uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
	gps = adafruit_gps.GPS(uart, debug=False)
	#gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0") #-minimal data
	gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')
	gps.send_command(b"PMTK220,1000")
	last_print = time.monotonic()
	while True:
		gps.update()
		current = time.monotonic()
		time.sleep(0.4)
		if current - last_print >= 1.0:
			last_print = current
			if not gps.has_fix:
				continue
			GPS_value = {
				"GPS" : 
				{
					"timestamp UTC": "{}.{}.{} {:02}:{:02}:{:02}".format(
					gps.timestamp_utc.tm_mon,
					gps.timestamp_utc.tm_mday,
					gps.timestamp_utc.tm_year,
					gps.timestamp_utc.tm_hour,
					gps.timestamp_utc.tm_min,
					gps.timestamp_utc.tm_sec,
					),
					"coordinates":
					{
						"longtitude": gps.longitude,
						"latitude": gps.latitude,
						"altitude": gps.altitude_m
					},
					"coordinates precise":
					{
						"longtitude": "{:2.0f}{:2.4f}".format(gps.longitude_degrees, gps.longitude_minutes),
						"latitude": "{:2.0f}{:2.4f}".format(gps.latitude_degrees, gps.latitude_minutes)
					},
					
					"speed": gps.speed_knots*0.51444,
					"fix data":
					{
						"fix quality": gps.fix_quality,
						"fix quality 3d": gps.fix_quality_3d,
					},
					"message number": gps.mess_num,
					"satellites data":
					{
						"satelites number": gps.satellites,
						"satelites details": gps.sats,
					},
					#"raw":gps
					
				}
			}


def read_sensor():
    global sensor_value
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

    while True:
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure

        sensor_value = {
            "BME280" : 
	        {
		"temperature": temperature,
                "humidity": humidity,
                "pressure": pressure
	        }
        }

        #print("Odczytuję dane z czujnika BME280...")
        time.sleep(1)


@app.get("/mainteance/temperature")
async def temperature():
	data = mainteance.getTemperature()
	if data is not None:
		return {"cpu temperature" : data}
	else:
		return Error_message

@app.get("/mainteance/volts")
async def volts():
	data = mainteance.getVolts()
	if data is not None:
		return {"cpu volts" : data}
	else:
		return Error_message

@app.get("/mainteance/clock")
async def clock():
	data = mainteance.getClock()
	if data is not None:
		return {"clocks" : data}
	else:
	    return Error_message
	
@app.get("/mainteance/display")
async def display():
	data = mainteance.getDisplay()
	if data is not None:
		return {"displays" : data}
	else:
	    return Error_message
	
@app.get("/mainteance/cpu")
async def cpuUsage():
	return {"Cpu usage":mainteance.getCpuUsage()}

@app.get("/mainteance/load")
async def loadAvg():
	return {"Load average":mainteance.getLoadAvg()}

@app.get("/mainteance/virtual_memory")
async def virtualMemory():
	return {"Virtual memory":mainteance.getVirtualMemory()}
	
@app.get("/mainteance/disk_usage")
async def diskUsage():
	return {"Disk usage":mainteance.getDiskUsage()}
	
@app.get("/mainteance/net_connections")
async def netConnections():
	return {"Net connections":mainteance.getNetworkConnections()}
	
@app.get("/mainteance/users")
async def users():
	return {"Users":mainteance.getCurrentUsers()}
	
@app.get("/mainteance/datetime")
async def datetime():
	return {"Time":mainteance.getDateTime()}
	
@app.get("/mainteance/mainteance")
async def getMainteance():
	return {"Full":mainteance.getFullMainteance()}
	
@app.get("/sensors/bme280")
async def get_sensor_value():
    global sensor_value
    if sensor_value is not None:
        return sensor_value
    else:
        return {"Error message": "Brak dostępnych danych z czujnika."}
    
@app.get("/sensors/gps")
async def get_gps_value():
    global GPS_value
    if GPS_value is not None:
        return GPS_value
    else:
        return {"Error message": "Brak dostępnych danych z GPS."}



sensor_thread = threading.Thread(target=read_sensor)
sensor_thread.start()

gps_thread = threading.Thread(target=read_GPS)
gps_thread.start()
