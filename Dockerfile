FROM python:3.9
WORKDIR /code
COPY ./setup.py /code/setup.py
RUN pip install .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./api /code/api
COPY ./pestcontrol /code/pestcontrol

COPY ./entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh
EXPOSE 80
RUN ["/code/entrypoint.sh"]
ENTRYPOINT ["uvicorn", "api.insect_detection_api:app", "--host", "0.0.0.0", "--port", "80"]

