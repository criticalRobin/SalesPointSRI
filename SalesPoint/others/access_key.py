from datetime import datetime
import re
import os
import django
import sys
import xml.etree.ElementTree as ET
import uuid

django_project_path = (
    "C:/Users/Matias/OneDrive/Escritorio/Data_Structure/SalesPoint/SalesPoint"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")
sys.path.append(django_project_path)
django.setup()
from SalesPoint.core.erp.models import Entity

class AccessKey:
    # uncluir el miso date de la venta
    current_date = datetime.now() 
    current_date_string = current_date.strftime("%d%m%Y")
    receipt_type = "01"
    ruc = ""
    enviroment_type = "1"
    bussiness_code = ""
    emition_code = ""
    series = bussiness_code + emition_code
    sequential_number = ""
    numerical_code = "12345678"
    emition_type = "1"
    verification_digit = ""
    
    

    def __init__(self, ruc, series, sequential_number):
        self.ruc = ruc
        self.series = series
        self.sequential_number = sequential_number

    def set_digit_verification(self, cdg48):
        if not cdg48.isdigit():
            return -1
        add = 0
        fac = 2
        for i in range(len(cdg48) - 1, -1, -1):
            if i == len(cdg48) - 1:
                add += int(cdg48[i]) * fac
            else:
                add += int(cdg48[i : i + 1]) * fac

            if fac == 7:
                fac = 2
            else:
                fac += 1

        dv = 11 - (add % 11)

        if dv == 10:
            return 1
        elif dv == 11:
            return 0
        return dv

    def generate_access_key(self):
        access_key_data = (
            self.current_date_string
            +self.receipt_type
            + self.ruc
            + self.enviroment_type
            + self.series
            + self.sequential_number
            + self.numerical_code
            + self.emition_type
        )
        verification_digit = self.set_digit_verification(access_key_data)
        self.verification_digit = str(verification_digit)
        return access_key_data + self.verification_digit

entity = Entity.objects.first()
ruc = entity.ruc
bussiness_code = entity.stablishement_code
emition_code = entity.emition_point_code
sequential_number = "000000008"
series = bussiness_code + emition_code
a = AccessKey(ruc, series, sequential_number)
key = a.generate_access_key()
print(a.set_digit_verification("280220230199999999999991001110000000003123456781")) 

