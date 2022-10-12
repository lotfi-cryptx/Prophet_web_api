# BigMama Prophet API

## What is done so far

This project is a python flask API which gives users capabilities to make forecasts on time series data using Facebook's Prophet library.
Multiple users can be added and each user can create and train multiple models.
The model training and forecasting is run on the server side.

## Documentation

For more details about how to use the API, please [Read The Documentation](https://app.swaggerhub.com/apis-docs/crptx/BigMama_Prophet_API/1.0.0).

## Deployment

To deploy the application, a docker image should be built first using:
```
docker build --tag bigmama_prophet_api:1.0.0 .
```
Then run new container using:
```
docker run --name {container_name} -p 5000:5000 -it bigmama_prophet_api:1.0.0
```


A docker container can also be pulled and ran directly from the remote [DockerHub repository](https://hub.docker.com/r/crptx/bigmama_prophet_api):
```
docker run --name {container_name} -p 5000:5000 -it crptx/bigmama_prophet_api:1.0.0-slim
```