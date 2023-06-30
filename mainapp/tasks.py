from celery import result, shared_task
import asyncio
from channels.consumer import get_channel_layer
import aiohttp
from asgiref.sync import sync_to_async
import requests
@shared_task(bind=True)
def my_task(self,coro_dict):
    datas={}
    for i in coro_dict:
           result=asyncio.run(update_stock(i))
           print(result)
           datas.update({i:result['Global Quote']})
    print(datas)
    #Sending data to frontend
    channel_layer = get_channel_layer()#It will get channel of specified user
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print(loop)
    if loop.is_running():
        print("The current loop is running!")
    loop.run_until_complete(channel_layer.group_send("chat_tracks", {#This will send data in chat_tracks group
        'type': 'send_stock_update',
        'message': datas,
    }))
    return "done"

    
async def update_stock(stockspicker):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop) 
    print(stockspicker)
    async with aiohttp.ClientSession() as session:
            API_KEY="IGT64HD5FBCS9ASB"
            url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey={}'
            r= await session.get(url.format(stockspicker,API_KEY),ssl=False)
            await asyncio.sleep(0.25)
            data = await r.json()
    return data

