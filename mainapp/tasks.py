from celery import result, shared_task
import asyncio
import aiohttp
from asgiref.sync import sync_to_async
import requests
@shared_task(bind=True)
def my_task(self,coro_dict):
    for i in coro_dict:
           result=asyncio.run(update_stock(i))
    return result

    
async def update_stock(stockspicker):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop) 
    print(stockspicker)
    datas={}
    async with aiohttp.ClientSession() as session:
            API_KEY="IGT64HD5FBCS9ASB"
            url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey={}'
            r= await session.get(url.format(stockspicker,API_KEY),ssl=False)
            await asyncio.sleep(0.25)
            data = await r.json()
            print(data)
            datas.update({stockspicker:data['Global Quote']})
            print(datas) 
    return "completed"

