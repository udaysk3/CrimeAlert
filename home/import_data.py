import pandas as pd
from models import YourData

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()

from django.core.management import call_command

def import_data():
    df = pd.read_csv('datasets\Districtwise_IPC_Crimes_2021.csv',encoding='utf-8')
    for _, row in df.iterrows():
        YourData.objects.create(
            District=row['District'],
            Murder=row['Murder'],
            Hurt=row['Hurt'],
            AssaultonWomen=row['AssaultonWomen'],
            KidnappingandAbduction=row['KidnappingandAbduction'],
            Rape=row['Rape'],
            UnlawfulAssembly=row['UnlawfulAssembly'],
            Theft=row['Theft'],
            Burglary=row['Burglary'],
            ForgeryCheatingFraud=row['ForgeryCheatingFraud'],
            OffencesRelatingtoDocumentsPropertyMarks=row['OffencesRelatingtoDocumentsPropertyMarks'],
            RashDrivingonPublicway=row['RashDrivingonPublicway'],
            CriminalTrespass=row['CriminalTrespass']
        )

if __name__ == "__main__":
    import_data()
