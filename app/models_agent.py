from datetime import datetime
from typing import Optional, List
from enum import IntEnum
from fastapi import FastAPI
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base


class RentalType(IntEnum):
    Bikes = 1
    Cars = 2
    BikeCars = 3
    Others = 4


class AddressType(IntEnum):
    Permenant = 1
    Current = 2


class Address(BaseModel):
    address_1: str
    address_2: str
    city: str
    state: str
    pincode: str
    country: str
    landmark: Optional[str] = None
    address_type: AddressType


class AgentIn(BaseModel):
    name: str
    description: Optional[str] = None
    address: List[Address]
    phone_office: str
    phone_mobile: str
    pancard: Optional[str] = None
    status: str
    contact_person: str
    rental_type: RentalType
    signup_ts: Optional[datetime] = None


class AgentOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    address: List[Address]
    phone_mob: str
    phone_land: Optional[str] = None
    PAN: Optional[str] = None
    status: str
    rental_type: RentalType
    signup_ts: Optional[datetime] = None


Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))
