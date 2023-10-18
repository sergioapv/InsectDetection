import sys
sys.path.insert(0, '../pestcontrol')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pestcontrol.settings")
import django
django.setup()
from insectcount.models import InsectCount
import datetime

class TrapMetrics():

    def __init__(self, inference_results: list):
        self.inference_results = inference_results
    
    def get_insect_quantity(self):
        """
        Returns the number of insects in the trap.
        """
        return len(self.inference_results[0].boxes)
    
    def get_insect_average_area(self):
        """
        Returns the average area of the insects in the trap in pixels.
        """
        average_area = 0
        for box in self.inference_results[0].boxes:
            w,h = box.xywh[0][2], box.xywh[0][3]
            average_area += w*h
        return average_area/self.get_insect_quantity()
    
    def get_insect_growth_rate(self, field_name: str, acquisition_time: datetime.datetime):
        """
        Get the growth rate of the insects in the trap in insects/hour.
        If the db is empty, returns 0.
        
        field_name: The name of the field where the trap is located.
        """
        if(len(InsectCount.objects.filter(field_name=field_name)) == 0):
            return 0
        last_insect_count = InsectCount.objects.filter(field_name=field_name).order_by('acquisition_date').reverse()[0]
        insect_dif = self.get_insect_quantity() - last_insect_count.insect_quantity
        time_dif = acquisition_time - last_insect_count.acquisition_date.replace(tzinfo=None)
        time_dif_hours = time_dif.seconds/3600
        return insect_dif/time_dif_hours