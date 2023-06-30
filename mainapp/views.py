from http.client import HTTPResponse
from django.shortcuts import render,redirect
from .models import Contactus
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render
import requests,csv
from asgiref.sync import sync_to_async
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
               val.append(row[0])
           val.pop(0)
           data=val
   except:
        data=["error","error","error"]
   return render(request,"index.html",{"stocks":data,"name":request.user.username})
@sync_to_async
def getloggedin(request):
   if request.method=="POST":
       username = request.POST.get("username")
       password = request.POST.get("password")
       user = authenticate(request, username=username, password=password)
       if user is not None:
          login(request, user)
          return redirect("index")
       else:
          return redirect("login")
   return render(request,"login.html")

def signup(request):
  if request.method=="POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      email = request.POST.get("email")
      if User.objects.filter(username = username).first():
         messages.error(request, "This username is already taken please chose diffrent username")
      else:
        user = User.objects.create_user(username, email, password)
        authenticate(request, username=username, password=password)
        user.save()
        return redirect("index")
  return render(request,"signup.html")

def Logout(request):
    logout(request)
    return redirect("index")

@sync_to_async
def get_all_users(request):
        if not request.user.is_authenticated:
                return False
        else:
                return True

async def stockspicked(request):
    is_loggedin=await get_all_users(request)
    print(is_loggedin)
    if not is_loggedin:
            return redirect("login")
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
