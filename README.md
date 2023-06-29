# stocktracker
Tracks current stocks using alpha_ventage api.Role of First url used as api in project is to get all current tickers list and second url is used to get ticker
details.Asyncronous programming is used to make rapid requests to api without waitinng for responses.Celery is used in this project in order to acquire
real time data.Whenever user submits the stocks our celery beat will get all those stock tickers and will keep on making api calls to get details about
stocks independently in every 20 seconds so that we can get real time deatails in every 20 seconds.Goal was to get data every 20 seconds but alpha_ventage
limitted the api calls up to 5 per/mins so we can only make 5 calls in every 60 seconds which is why I reccomend to select only 5 stocks for now but you can
buy premium pakage of alpha_ventage to change that.Once all details is acquired we will use django channels and websockets to get those details in frontend.Project is still uncomplete

# Workflow:
At first I created a group named chat_tracks inside consumers.py vwhich contains channel_layers of all user/clients in our websocket.
Whenever user comes websocket page with some selected stocks from previous page,I will add that user's channel_layer inside my chat_tracks group
and I will create a task(If not present) using those selected stocks selected by user as an argument to task or I will just change the argument if task
is present.In that task named mytask I will call api which will get all details about those selected stocks and I will send those details to user who
made the request using group_send method.When I use group_send method at first I will send those details to chat_tracks group which contains all the uses/clients 
channel_layer from that group I can send those data to user which made the request.I created group because whenever two or more users/clients inside that group 
asks for details about same stocks then I can make only one api call for those users and  boardcast those details to users through group.Once I send that details to specified
channel_layer in my backend I will use websocket to send that details to frontend to that specified user/client/channel_layer.In consumer.py I have made specifications to 
delete the task if there is no argument,delete the stocks which are not selected by specific user,delete the user if it is disconnected from the websocket.In this way I can
prevent data clash between two users.
