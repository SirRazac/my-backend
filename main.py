from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SensorData(BaseModel):
    temperature: float
    humidity: float

@app.get("/api/data", response_model=SensorData)
async def get_sensor_data():
    # simulated data
    return SensorData(temperature=25.0, humidity=60.0)
