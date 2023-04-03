import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from bson.json_util import dumps
from typing import Optional, List
from pymongo import MongoClient
from datetime import datetime
import json
import traceback
import logging

logging.basicConfig(filename="debug.log")

app = FastAPI()
mongo_uri = f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}/?ssl=true&retrywrites=false"
client  = MongoClient(mongo_uri)

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class SensorData(BaseModel):
    timestamp: str = Field(default_factory=lambda: str(datetime.utcnow()))
    sensor_1: float = Field(...)
    sensor_2: float = Field(...)
    sensor_3: float = Field(...)
    sensor_4: float = Field(...)
    sensor_5: float = Field(...)
    sensor_6: float = Field(...)
    sensor_7: float = Field(...)
    sensor_8: float = Field(...)
    sensor_9: float = Field(...)
    sensor_10: float = Field(...)

class PatientData(BaseModel):
    id: int = Field(...)
    Name: str = Field(...)
    Age: int = Field(...)
    Address: str = Field(...)
    Status: str = Field(...)

@app.post("/add_many/{collection}/{db}", response_description="Add many sensors")
async def add_many_sensors(
    collection: str,
    db: str,
    sensors: List[SensorData] = Body(...),
):
    db_client = MongoClient(mongo_uri)
    db = db_client[db]
    collection = db[collection]

    try:
        # Convert sensor data to JSON compatible format
        sensor_docs = jsonable_encoder(sensors)
        print(sensor_docs)

        # Insert multiple documents into collection
        result = collection.insert_many(sensor_docs)
        
        # Return the IDs of the inserted documents
        return {'inserted_ids': [str(i) for i in result.inserted_ids]}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=traceback.format_exc())
    

@app.post("/add_many/patient/{db}/{collection}", response_description="Add many sensors")
async def add_patients(
    collection: str,
    db: str,
    sensors: List[PatientData] = Body(...),
):
    db_client = MongoClient(mongo_uri)
    db = db_client[db]
    collection = db[collection]

    try:
        # Convert sensor data to JSON compatible format
        sensor_docs = jsonable_encoder(sensors)
        print(sensor_docs)

        # Insert multiple documents into collection
        result = collection.insert_many(sensor_docs)
        
        # Return the IDs of the inserted documents
        return {'inserted_ids': [str(i) for i in result.inserted_ids]}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=traceback.format_exc())

@app.get("/all/{db}/{collection}", response_description="Retrieve all records within collection")
async def retrieve_all_records(db: str, collection: str):
    client = MongoClient(mongo_uri)
    db = client[db]
    collection = db[collection]

    # Find all documents in the collection and convert them to a JSON string
    cursor = collection.find({})
    json_docs = dumps(cursor)

    return JSONResponse(content=json.loads(json_docs))



# @app.post("/add", response_description="Add one sensor")
# async def create_one_record():
#     pass

# @app.get("/one/{id}", response_description="Add one sensor")
# async def retreive_one_record():
#     pass



# @app.put("/update/{id}", response_description="Add one sensor")
# async def update_one():
#     pass