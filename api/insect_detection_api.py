from ultralytics import YOLO
from fastapi import FastAPI, Body
import requests
import asyncio
import sys
import sys
sys.path.insert(0, '../pestcontrol')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pestcontrol.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
django.setup()
from insectcount.models import InsectCount
import datetime
import numpy as np
from trap_metrics import TrapMetrics
from typing import Union, Annotated

app = FastAPI()

def run_inference(model_path, file_path, imgsz, conf):
    model = YOLO(model_path)  # predict on an image
    results = model(file_path, save=True, imgsz=imgsz, conf=conf)
    return results

@app.get("/{field_name}/{trap_id}")
async def trap_metrics(file_url : str, 
                 acquisition_date : Union[str, None] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 field_name : str = None,
                 trap_id : str = None,
                 ):
    
    img_data = requests.get(file_url).content
    with open('inference.jpg', 'wb') as handler:
        handler.write(img_data)

    if acquisition_date is None:
        acquisition_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if type(acquisition_date) is str:
        acquisition_date = datetime.datetime.strptime(acquisition_date, "%Y-%m-%d %H:%M:%S")

    # Inference
    results = run_inference("/home/sergio/Documents/Repositories/InsectDetectionServer/models/best.pt", 'inference.jpg', 320, 0.1)  # load a pretrained model (recommended for training)   

    # Get metrics
    insect_metrics = TrapMetrics(results)
    insect_quantity = insect_metrics.get_insect_quantity()
    average_insect_area = insect_metrics.get_insect_average_area()
    insect_growth_rate = insect_metrics.get_insect_growth_rate(field_name, acquisition_date)

    #save to database
    insect_count = InsectCount(acquisition_date = acquisition_date, insect_quantity = insect_quantity, insect_area = average_insect_area, field_name = field_name, trap_id = trap_id)
    insect_count.save()

    return {"Insects": insect_quantity,
            "Average_insect_area": average_insect_area,
            "insect_growth_rate": insect_growth_rate,
    }

print(trap_metrics(file_url = 'https://raw.githubusercontent.com/md-121/yellow-sticky-traps-dataset/main/images/1000.jpg', field_name='test', trap_id=1))