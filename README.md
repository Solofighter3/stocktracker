# stocktracker
Tracks current stocks using alpha_ventage api.Role of First url used as api in project is to get all current tickers list and second url is used to get ticker
details.Asyncronous programming is used to make rapid requests to api without waitinng for responses.Celery is used in this project in order to acquire
real time data.Whenever user submits the stocks our celery beat will get all those stock tickers and will keep on making api calls to get details about
stocks independently in every 20 seconds so that we can get real time deatails in every 20 seconds.Project is still uncomplete

Workflow:
At first I created a group named chat_tracks inside consumers.py vwhich contains channel_layers of all user/clients in our websocket.
Whenever user comes websocket page with some selected stocks from previous page,I will add that user's channel_layer inside my chat_tracks group
and I will create a task(If not present) using those selected stocks selected by user as an argument to task or I will just change the argument if task
is present.In that task named mytask I will call api which will get all details about those selected stocks and I will send those details to group
chat_tracks using group send.chat_tracks contains all the uses/clients channel_layer so we can 
