from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing import Any, Dict, Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler: Any) -> core_schema.CoreSchema:
        return core_schema.str_schema()

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: core_schema.CoreSchema, handler: Any) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update({'type': 'string', 'examples': ['60d5f0b5f5d3c2f1d7e2c3d4']})
        return json_schema


def _serialize_objectid(v: Any) -> str:
    return str(v) if isinstance(v, ObjectId) else v



class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,
                           alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class CarBase(MongoBaseModel):

    brand: str = Field(..., min_length=3)
    make: str = Field(..., min_length=3)
    year: int = Field(..., gt=1975, lt=2023)
    price: int = Field(...)
    km: int = Field(...)
    cm3: int = Field(...)


class CarUpdate(MongoBaseModel):
    price: Optional[int] = None


class CarDB(CarBase):
    pass

if __name__ == '__main__':
    car = {
        'brand': 'Ford',
        'make': 'Focus',
        'year': 2010,
        'price': 5000,
        'km': 100000,
        'cm3': 1600}
    cbd = CarDB(**car)
    encoded_car = jsonable_encoder(cbd)
    print(encoded_car)
