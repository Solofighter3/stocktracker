from django.shortcuts import render,redirect
from .models import Contactus
from django.contrib import messages
from django.shortcuts import render
import requests,csv
from alpha_vantage.timeseries import TimeSeries
import asyncio
import aiohttp
def index(request):
   try:
       CSV_URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo'
       with requests.Session() as s:
           download = s.get(CSV_URL)
           decoded_content = download.content.decode('utf-8')
           cr = csv.reader(decoded_content.splitlines(), delimiter=',')
           my_list = list(cr)
           val=[]
           for row in my_list:
               print(row[0])
               val.append(row[0])
           val.pop(0)
           data=val
   except:
        data=["error","error","error"]
   return render(request,"index.html",{"stocks":data})

async def stockspicked(request):
    stockspicker=request.GET.getlist("stockspicker")
    print(stockspicker)
    datas={}
    try:
      async with aiohttp.ClientSession() as session:
         for i in stockspicker:
            API_KEY="IGT64HD5FBCS9ASB"
            url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey={}'
            r= await session.get(url.format(i,API_KEY),ssl=False)
            await asyncio.sleep(0.25)
            data = await r.json()
            print(data)
            datas.update({i:data['Global Quote']})
    except:
         pass
    return render(request,"stocks.html",{'data':datas,"room_name":"tracks"})



def contacts(request):
   if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        text=request.POST.get("desc")
        contact=Contactus(name=username,email=email,text=text)
        contact.save()
        messages.success(request, 'Profile details updated.')
   
   return render(request,"contact.html")
