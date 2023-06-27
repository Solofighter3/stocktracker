# stocktracker
Tracks current stocks using alpha_ventage api.Role of First url used as api in project is to get all current tickers list and second url is used to get ticker
details.Asyncronous programming is used to make rapid requests to api without waitinng for responses.Celery is used in this project in order to acquire
real time data.Whenever user submits the stocks our celery beat will get all those stock tickers and will keep on making api calls to get details about
stocks independently in every 20 seconds so that we can get real time deatails in every 20 seconds.Project is still uncomplete
