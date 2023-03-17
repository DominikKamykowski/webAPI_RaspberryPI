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
