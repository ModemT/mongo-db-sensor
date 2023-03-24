export MONGODB_URL="mongodb://modemss:opH9opk5PIFjYVlzJ3JsnslgzvywXrUsDOqo0ZgTDced6DoFHLqJ0XRdutfjXqTKx66qrRFTVQw9ACDbdmau5w==@modemss.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@modemss@"
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
