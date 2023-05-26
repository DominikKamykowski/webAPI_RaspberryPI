from fastapi import FastAPI
from Mainteance import Mainteance
import threading
import time
import board
import busio
import adafruit_bme280

app = FastAPI()
mainteance = Mainteance()
sensor_value = None

def read_sensor():
    global sensor_value
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    while True:
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure

        sensor_value = {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure
        }

        #print("Odczytuję dane z czujnika BME280...")
        time.sleep(2)


@app.get("/mainteance/temperature")
async def temperature():
	return {"cpu temperature" : mainteance.getTemperature()}

@app.get("/mainteance/volts")
async def volts():
	return {"cpu volts" : mainteance.getVolts()}
	
@app.get("/mainteance/clock")
async def clock():
	return {"clocks":mainteance.getClock()}
	
@app.get("/mainteance/display")
async def display():
	return {"displays":mainteance.getDisplay()}
	
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
        return {"message": "Brak dostępnych danych z czujnika."}

sensor_thread = threading.Thread(target=read_sensor)
sensor_thread.start()