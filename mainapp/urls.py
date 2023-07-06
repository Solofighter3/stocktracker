from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('stocks',views.stockspicked,name="stockspicked"),
    path('contacts/',views.contacts,name="contacts"),
    path('login/',views.getloggedin,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.Logout,name="logout"),
   ]
