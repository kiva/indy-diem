import diem 
import asyncio

from diem.jsonrpc import AsyncClient

JSON_RPC_URL = "http://127.0.0.1:8080"

async def main():
    with AsyncClient(JSON_RPC_URL) as client:
        print(await client.get_metadata())

asyncio.run(main())