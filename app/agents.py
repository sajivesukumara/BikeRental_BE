from datetime import datetime
from typing import Optional, List
from enum import IntEnum
from fastapi import FastAPI
from pydantic import BaseModel

from models_agent import AgentIn, AgentOut, Address, AddressType

from db import dbapi

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Home Page"}


agent_1001_addr = Address(address_1="MG Road", address_2="Utility Building",
                          pincode="560043", state="West Bengal",
                          city="Siliguri", country="India",
                          address_type=AddressType.Permenant)

agent_1001 = AgentOut(id=1001, name="Himalaya Bikers",
                      description="Sikkim bike rentals",
                      address=[agent_1001_addr],
                      phone_mob="+91 9876543210",
                      status="Active",
                      rental_type=AddressType.Permenant,
                      signup_ts="2020-12-21T10:20:30.400+02:30")

agent_2001_addr = Address(address_1="Richmond Road", address_2="Park Square",
                          pincode="360043", state="West Bengal",
                          city="Siliguri", country="India",
                          address_type=AddressType.Permenant)

agent_2001 = AgentOut(id=2001, name="Eagle Riders",
                      description="Sikkim bike rentals",
                      address=[agent_2001_addr],
                      phone_mob="+91 9876543210",
                      status="Active",
                      rental_type=AddressType.Permenant,
                      signup_ts="2020-12-21T10:20:30.400+02:30")

agent_3001_addr = Address(address_1="ITPL Road", address_2="Eagle Towers",
                          pincode="360043", state="West Bengal",
                          city="Siliguri", country="India",
                          address_type=AddressType.Permenant)

agent_3001 = AgentOut(id=2001, name="Siliguri Rentals",
                      description="Siliguri bike and car rentals",
                      address=[agent_3001_addr],
                      phone_mob="+91 9876543210",
                      status="Active",
                      rental_type=AddressType.Permenant,
                      signup_ts="2020-12-21T10:20:30.400+02:30")

agent = [agent_1001, agent_2001, agent_3001]


@app.post("/agents/")
async def create_item(agent: AgentIn):
    #dbapi.add_agency(None, agent)

    values = {
        'name': 'agency20',
        'address1': 'SKS Orchid',
        'address2': 'HSR Layout',
        'city': 'Siliguri',
        'state': 'WB',
        'pincode': '234567',
        'country': 'India',
        'phone_office': '9867232000',
        'phone_mobile': '080-984000',
        'contact_person': 'John',
        'rental_type': 1,
        'status': 'Active'
    }
    dbapi.create_agency(None, values)
    return "new agency added"
    #return agent


@app.get("/agents")
async def get_Agents():
    result_set = dbapi.get_agency()
    print(result_set)
    agents = []
    for r in result_set:
        agents.append(r)
    return agents


@app.get("/agents/{agent_id}", response_model=AgentOut,
         response_model_exclude_unset=True)
async def get_agent_id(agent_id: int):
    agentFound = agent[agent_id]
    agentFound.id = 200

    return agent[agent_id]
