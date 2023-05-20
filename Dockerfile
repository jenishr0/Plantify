FROM python:3.10

RUN mkdir -p /indoor_plants

COPY . /indoor_plants/

RUN python3 -m pip install -r /indoor_plants/requirements.txt

EXPOSE 5000

CMD ["python", "/indoor_plants/app.py"]