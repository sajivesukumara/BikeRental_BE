__author__ = 'sajive'
from datetime import datetime
from typing import Optional, List
from enum import IntEnum
from fastapi import FastAPI, APIRouter, Depends
from ..dependencies import get_query_token, get_token_header
from pydantic import BaseModel
from ..models_agent import AgentIn, AgentOut, Address, AddressType
from ..db import dbapi
import logging

logging.basicConfig()
logging.getLogger('agency').setLevel(logging.INFO)

app = APIRouter(
    prefix="/agents",
    tags=["agents"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@app.post("/")
async def create_item(agent: AgentIn):
    #dbapi.add_agency(None, agent)
    print("=============================================")
    print(agent)
    print("=============================================")
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


@app.get("/")
async def get_Agents():
    result_set = dbapi.get_agency()
    print(result_set)
    agents = []
    for r in result_set:
        agents.append(r)
    return agents


@app.get("/{agent_id}", response_model=AgentOut,
         response_model_exclude_unset=True)
async def get_agent_id(agent_id: int):
    agentFound = agent[agent_id]
    agentFound.id = 200

    return agent[agent_id]
