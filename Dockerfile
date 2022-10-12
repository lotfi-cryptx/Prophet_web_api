FROM python:3.7-stretch

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 --no-cache-dir install -r requirements.txt && pip3 --no-cache-dir install fbprophet

COPY ./Flask_app .

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host", "0.0.0.0"]