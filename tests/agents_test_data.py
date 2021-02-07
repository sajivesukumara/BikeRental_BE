
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

