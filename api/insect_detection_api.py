from ultralytics import YOLO
from fastapi import FastAPI, Body
import requests
import asyncio
import sys
import sys
sys.path.insert(0, 'pestcontrol')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pestcontrol.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
django.setup()
from insectcount.models import InsectCount
import datetime
import numpy as np
from api.trap_metrics import TrapMetrics
from typing import Union, Annotated

app = FastAPI()

def run_inference(model_path, file_path, imgsz, conf):
    model = YOLO(model_path)  # predict on an image
    results = model(file_path, save=True, imgsz=imgsz, conf=conf)
    return results

@app.get("/insect_metrics/{field_name}/{trap_id}/")
async def trap_metrics(file_url : str, 
                 acquisition_date : Union[str, None],
                 field_name : str,
                 trap_id : str
                 ):
    """
    This function takes an image url and returns the number of insects, the average insect area and the insect growth rate.

    Parameters
    ----------
    file_url : str 
        The url of the image to be processed.
    acquisition_date : str, optional
        The date the image was taken. If not provided, the current date will be used.
    field_name : str, optional
        The name of the field where the trap is located.
    trap_id : str, optional
        The id of the trap.
    """
    
    # Download image
    img_data = requests.get(file_url).content
    with open('inference.jpg', 'wb') as handler:
        handler.write(img_data)

    # Acquire date if not provided
    if acquisition_date is None:
        acquisition_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if type(acquisition_date) is str:
        acquisition_date = datetime.datetime.strptime(acquisition_date, "%Y-%m-%d %H:%M:%S")

    # Run inference and get metrics
    inference_results = run_inference("/models/best.pt", 'inference.jpg', 320, 0.1)
    insect_metrics = TrapMetrics(inference_results, acquisition_date, field_name, trap_id).yield_metrics()

    #save object to database
    insect_count = InsectCount(acquisition_date = acquisition_date, 
                               insect_quantity = insect_metrics['insect_quantity'], 
                               insect_area = insect_metrics['average_insect_area'], 
                               field_name = field_name, 
                               trap_id = trap_id)
    insect_count.save()

    return insect_metrics
