#from main1 import database
import databases
import asyncio
from data.user import table_of_users


async def execution():
    database = databases.Database("postgresql://jmbwrqtkciptar:49a7cc52b929258ba0667f13e3227601473c1245ef78dd5965ced615442a1dc0@ec2-52-214-178-113.eu-west-1.compute.amazonaws.com:5432/d3vhsjgllvb4ht")
    await database.connect()
    query = table_of_users.delete()
    await database.execute(query)
    
    
asyncio.run(execution())