from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
# Create your views here.
def home(request):
    return render(request,'index.html')

# Create your views here.
matplotlib.use('Agg')
def plot_bar_district_chart(target_district):
    data = pd.read_csv("static/dataset/IPC_Crimes_2020.csv")
    district_data = data[data["District"] == target_district]
    district_data = district_data.drop(columns=["District"])
    plt.figure(figsize=(12, 8))
    plt.bar(district_data.columns, district_data.iloc[0])
    plt.xlabel("Crime Type")
    plt.ylabel("Count")
    plt.title(f"Crime Type Comparison in {target_district}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    img_tag = f'<img width="500px" src="data:image/png;base64,{image_base64}" />'
    return img_tag

def plot_pie_district_chart(target_district):
    data = pd.read_csv("static/dataset/IPC_Crimes_2020.csv")
    district_data = data[data["District"] == target_district]
    district_data = district_data.drop(columns=["District"])
    crime_types = district_data.columns
    crime_counts = district_data.iloc[0]
    plt.figure(figsize=(10, 8))
    plt.pie(crime_counts, labels=crime_types, autopct="%1.1f%%", startangle=140)
    plt.title(f"Crime Type Distribution in {target_district}")
    plt.axis("equal")
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    img_tag = f'<img width="500px" src="data:image/png;base64,{image_base64}" />'
    return img_tag
    
def plot_bar_districts_chart(districts):
        data = pd.read_csv("static/dataset/IPC_Crimes_2020.csv")
        filtered_data = data[data["District"].isin(districts)]
        grouped_data = filtered_data.groupby("District").sum()
        crime_types = grouped_data.columns
        crime_counts_district_a = grouped_data.loc[districts[0]]
        crime_counts_district_b = grouped_data.loc[districts[1]]
        x = np.arange(len(crime_types))
        bar_width = 0.35
        plt.figure(figsize=(10, 6))
        plt.bar(x - bar_width/2, crime_counts_district_a, bar_width, label=districts[0])
        plt.bar(x + bar_width/2, crime_counts_district_b, bar_width, label=districts[1])
        plt.xlabel("Crime Type")
        plt.ylabel("Count")
        plt.title(f"Crime Type Comparison between {districts[0]} and {districts[1]}")
        plt.xticks(x, crime_types, rotation=45)
        plt.legend()
        plt.tight_layout()
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()
        image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
        img_tag = f'<img width="500px" src="data:image/png;base64,{image_base64}" />'
        return img_tag
def crimestatistics(request):
    if request.method == "POST":
        if request.POST['type'] == 'district':
            target_district = request.POST["district"]
            images = []
            images.append(plot_bar_district_chart(target_district))
            images.append(plot_pie_district_chart(target_district))
            return render(request, "why.html", {"district": True, "images": images})
        if request.POST['type'] == 'district2':
            districts = []
            districts.append(request.POST["district1"])
            districts.append(request.POST["district2"])
            images = []
            images.append(plot_bar_districts_chart(districts))
            return render(request, "why.html", {"district": True, "images": images})
    return render(request, 'why.html')


