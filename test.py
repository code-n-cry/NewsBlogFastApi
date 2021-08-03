from app.main1 import database
import asyncio
from app.data.user import table_of_tokens, table_of_users


async def execution():
    await database.connect()
    query = table_of_users.delete()
    await database.execute(query)
    query2 = table_of_tokens.delete()
    await database.execute(query2)
    
    
asyncio.run(execution())