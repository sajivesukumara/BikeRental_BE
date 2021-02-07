from datetime import datetime
from typing import Optional, List
from enum import IntEnum
from fastapi import FastAPI
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from ..db.common import ModelBase


Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class AgencyOrm(Base, ModelBase):
    __tablename__ = 'agency'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), index=True, nullable=False, unique=True)
    description = Column(String(256))
    phone_office = Column(String(63))
    phone_mobile = Column(String(63))
    pancard = Column(String(63))
    status = Column(String(63))
    contact_person = Column(String(63))
    rental_type = Column(String(32))
    signup_ts = Column(Date)
    address1 = Column(String(63))
    address2 = Column(String(63))
    city = Column(String(63))
    state = Column(String(63))
    country = Column(String(63))
    pincode = Column(String(63))


class CustomersOrm(Base, ModelBase):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(20), index=True, nullable=False, unique=True)
    last_name = Column(String(20), index=True, nullable=False, unique=True)
    middle_name = Column(String(20), index=True)
    dob = Column(Date)
    address = Column(String(256))
    id_proof = Column(String(32))
    driving_license = Column(String(32))
    phone_mobile = Column(String(16))
    email = Column(String(16))


class BikesOrm(Base):
    __tablename__ = 'bikes'
    id = Column(Integer, primary_key=True, nullable=False)
    agency_id = Column(Integer, nullable=False)
    registration = Column(String(16), nullable=False)
    status = Column(String(16), nullable=False)
    model = Column(String(16), nullable=False)
    make = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    last_service_date = Column(Date, nullable=False)
    insurance = Column(String(16), nullable=False)
    riding_capacity = Column(Integer, nullable=False)
    total_km = Column(Integer, nullable=False)
    fuel = Column(String(16), nullable=False)
    milage = Column(Integer, nullable=False)
    model = Column(String(16), nullable=False)
    cc = Column(Integer, nullable=False)
    color = Column(String(16), nullable=False)


# The vehicles rented by customers
class RentalsOrm(Base, ModelBase):
    __tablename__ = 'rentals'
    id = Column(Integer, primary_key=True, nullable=False)  # PK
    customer_id = Column(Integer, ForeignKey(
        'CustomersOrm.id'), nullable=False)
    bike_id = Column(Integer, ForeignKey('BikesOrm.id'), nullable=False)
    start_date = Column(Date,  nullable=False)
    end_date = Column(Date,  nullable=False)
    destination = Column(String(50), nullable=False)
    booking_ref = Column(String(32), nullable=False)
    booking_status = Column(String(16), nullable=False)
    payment_status = Column(String(16), nullable=False)
    customer = relationship(CustomersOrm, backref="rentals",
                          foreign_keys=customer_id,
                          primaryjoin='and_('
                          'RentalsOrm.customer_id == CustomersOrm.id,'
                          'RentalsOrm.deleted == False)', lazy='joined',
                          join_depth=4)


class BikePricesOrm(Base):
    __tablename__ = 'bike_prices'
    id = Column(Integer, primary_key=True, nullable=False)


class BikeAdditionalInfoOrm(Base):
    __tablename__ = 'bike_additional_info'
    id = Column(Integer, primary_key=True, nullable=False)


class PaymentDetailsOrm(Base):
    __tablename__ = 'payment_details'
    id = Column(Integer, primary_key=True, nullable=False)
