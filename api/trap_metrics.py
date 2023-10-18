import sys
sys.path.insert(0, '../pestcontrol')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pestcontrol.settings")
import django
django.setup()
from insectcount.models import InsectCount
import datetime

class TrapMetrics():

    def __init__(self, inference_results: list, acquisition_date: datetime.datetime, field_name: str = None, trap_id: int = None):
        self.inference_results = inference_results
        self.acquisition_date = acquisition_date
        self.field_name = field_name
        self.trap_id = trap_id
    
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
    
    def get_insect_growth_rate(self):
        """
        Get the growth rate of the insects in the trap in insects/hour.
        If the db is empty, returns 0.
        
        Parameters
        ----------
        field_name: str 
            The name of the field where the trap is located.
        acquisition_time: datetime.datetime
            The time when the image was taken.
        """
        #return 0 if there arent records from that trap
        if(len(InsectCount.objects.filter(field_name=self.field_name, trap_id = self.trap_id)) == 0):
            return 0
        #get latest acquisition
        last_insect_count = InsectCount.objects.filter(field_name=self.field_name, trap_id = self.trap_id).order_by('acquisition_date').reverse()[0]
        #calculate growth rate
        insect_dif = self.get_insect_quantity() - last_insect_count.insect_quantity
        time_dif = self.acquisition_date - last_insect_count.acquisition_date.replace(tzinfo=None)
        if(time_dif.seconds <= 0):
            return 0
        time_dif_hours = time_dif.seconds/3600
        return insect_dif/time_dif_hours
    
    def yield_metrics(self):
        """
        Returns a dictionary with the number of insects, the average insect area and the insect growth rate.
        """
        return {
            'insect_quantity': self.get_insect_quantity(),
            'average_insect_area': self.get_insect_average_area(),
            'insect_growth_rate': self.get_insect_growth_rate()
        }