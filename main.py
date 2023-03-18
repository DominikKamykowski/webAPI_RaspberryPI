from fastapi import FastAPI
from Mainteance import Mainteance

app = FastAPI()
mainteance = Mainteance()


@app.get("/mainteance/temperature")
async def temperature():
	return {"cpu temperature" : mainteance.getTemperature()}

@app.get("/mainteance/volts")
async def volts():
	return {"cpu volts" : mainteance.getVolts()}
	
@app.get("/mainteance/clock")
async def clock():
	return mainteance.getClock()
	
@app.get("/mainteance/display")
async def display():
	return mainteance.getDisplay()
	
@app.get("/mainteance/cpu")
async def cpuUsage():
	return mainteance.getCpuUsage()

@app.get("/mainteance/load")
async def loadAvg():
	return mainteance.getLoadAvg()

@app.get("/mainteance/virtual_memory")
async def virtualMemory():
	return mainteance.getVirtualMemory()
	
@app.get("/mainteance/disk_usage")
async def diskUsage():
	return mainteance.getDiskUsage()
	
@app.get("/mainteance/net_connections")
async def netConnections():
	return mainteance.getNetworkConnections()
	
@app.get("/mainteance/users")
async def users():
	return mainteance.getCurrentUsers()
	
@app.get("/mainteance/datetime")
async def datetime():
	return mainteance.getDateTime()
