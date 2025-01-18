from fastapi import FastAPI, HTTPException
import Adafruit_DHT
from pydantic import BaseModel

app = FastAPI()

SENSOR = Adafruit_DHT.DHT22
PIN = 4

class SensorData(BaseModel):
    temperature: float
    humidity: float

@app.get("/api/data", response_model=SensorData)
async def get_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    if humidity is not None and temperature is not None:
        return SensorData(temperature=temperature, humidity=humidity)
    else:
        raise HTTPException(status_code=500, detail="Sensor read failed")
