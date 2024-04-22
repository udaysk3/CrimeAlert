from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
import pandas as pd
import matplotlib
from accounts.models import User
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
from geopy.geocoders import Nominatim
import joblib
from .forms import ScamReportForm
from .models import ScamReport

def predict(request):
    if request.method == "POST":
        address = request.POST['location']
        geolocator = Nominatim(user_agent='crime')
        location = geolocator.geocode(address, timeout=None)
        print(location.address)
        lat = [location.latitude]
        log = [location.longitude]
        latlong = pd.DataFrame({'latitude': lat, 'longitude': log})
        print(latlong)
        
        rfc = joblib.load('home/model.pkl')
        DT = request.POST['timestamp']
        latlong['timestamp'] = DT
        data = latlong
        cols = data.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        data = data[cols]

        data['timestamp'] = pd.to_datetime(data['timestamp'].astype(str), errors='coerce')
        column_1 = data.loc[:, data.columns[0]]
        DT = pd.DataFrame({
            "month": column_1.dt.month,
            "day": column_1.dt.day,
            "hour": column_1.dt.hour,
            "dayofyear": column_1.dt.dayofyear,
            # "week":  (column_1.dt.day - 1) // 7 + 1,  # Get week
            "week": column_1.dt.isocalendar().week,  # Get week of the year
            "weekofyear": column_1.dt.isocalendar().week,  # Get week of the year
        })
        data = data.drop('timestamp', axis=1)
        final = pd.concat([DT, data], axis=1)
        print(final)
        X = final.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7]].values
        my_prediction = rfc.predict(X)
        if my_prediction[0][0] == 1:
            my_prediction = 'Predicted crime : Act 379-Robbery'
        elif my_prediction[0][1] == 1:
            my_prediction = 'Predicted crime : Act 13-Gambling'
        elif my_prediction[0][2] == 1:
            my_prediction = 'Predicted  : Act 279-Accident'
        elif my_prediction[0][3] == 1:
            my_prediction = 'Predicted crime : Act 323-Violence'
        elif my_prediction[0][4] == 1:
            my_prediction = 'Predicted crime : Act 302-Murder'
        elif my_prediction[0][5] == 1:
            my_prediction = 'Predicted crime : Act 363-kidnapping'
        else:
            my_prediction = 'Place is safe no crime expected at that timestamp.'
        print(my_prediction)
        context = my_prediction
        return render(request, 'predict.html', {'prediction': context})
    
    return render(request, 'predict.html')


def display_scam_reports(request):
    if request.method == 'POST':
        selected_district = request.POST.get('district')
        scam_reports = ScamReport.objects.filter(district=selected_district)
        return render(request, 'scam_reports.html', {'scam_reports': scam_reports, 'selected_district': selected_district})
    else:   
        return render(request, 'district.html')

def scam_report(request):
    if request.method == 'POST':
        form = ScamReportForm(request.POST, request.FILES)
        if form.is_valid():
            scam_report = form.save(commit=False)
            scam_report.user = request.user
            scam_report.save()
            return redirect('/')  # Redirect to a success page
    else:
        form = ScamReportForm()
    return render(request, 'report.html', {'form': form})


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        scams = list(ScamReport.objects.filter(district=request.user.district).values())
        for scam in scams:
            scam["user"] = User.objects.get(id=scam["user_id"]).username
        request.session["scams"] = scams
        return render(request,'index.html')
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
    img_tag = f'<img width="1000px" src="data:image/png;base64,{image_base64}" />'
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
    img_tag = f'<img width="1000px" src="data:image/png;base64,{image_base64}" />'
    return img_tag

def plot_bar_districtyear_chart(target_district):
    df_year1 = pd.read_csv('static/dataset/Districtwise_IPC_Crimes_2021.csv')
    df_year2 = pd.read_csv('static/dataset/IPC_Crimes_2020.csv')

    district_name = target_district
    df_district_year1 = df_year1[df_year1['District'] == district_name]
    df_district_year2 = df_year2[df_year2['District'] == district_name]


    year1 = df_district_year1.iloc[0, 1:]
    year2 = df_district_year2.iloc[0, 1:]

    year1 = year1.astype(int)
    year2 = year2.astype(int)



    comparison_df = pd.DataFrame({
        '2021': year1,
        '2020': year2
    })

    comparison_df.reset_index(inplace=True)

    comparison_df.plot(x='index', kind='bar', figsize=(13, 9))
    plt.title(f'Crime Type Comparison for {district_name} (2021 vs. 2020)')
    plt.xlabel('Crime Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    img_tag = f'<img width="1000px" src="data:image/png;base64,{image_base64}" />'
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
        img_tag = f'<img width="1000px" src="data:image/png;base64,{image_base64}" />'
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
        img_tag = f'<img width="1000px" src="data:image/png;base64,{image_base64}" />'
        return img_tag
def plot_bar_state_chart(state):
    data = pd.read_csv("static/dataset/States_IPC_Crimes_2021.csv")
    target_state = state
    print(target_state)
    state_data = data[data["State"] == target_state]

    state_data = state_data.drop(columns=["State"])
    plt.figure(figsize=(14, 8))
    plt.bar(state_data.columns, state_data.iloc[0])
    plt.xlabel("Crime Type")
    plt.ylabel("Count")
    plt.title(f"Crime Type Comparison in {target_state}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    img_tag = f'<img width="1000px" src="data:image/png;base64,{image_base64}" />'
    return img_tag
def plot_pie_state_chart(state):
    data = pd.read_csv("static/dataset/States_IPC_Crimes_2021.csv")
    target_state = state
    print(target_state)
    state_data = data[data["State"] == target_state]
    state_data = state_data.drop(columns=["State"])
    crime_types = state_data.columns
    crime_counts = state_data.iloc[0]
    plt.figure(figsize=(14, 10))
    plt.pie(crime_counts, labels=crime_types, autopct="%1.1f%%", startangle=140)
    plt.title(f"Crime Type Distribution in {target_state}")
    plt.axis("equal")
    plt.show()
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    img_tag = f'<img width="1000px" src="data:image/png;base64,{image_base64}" />'
    return img_tag
def crimestatistics(request):
    if request.method == "POST":
        if request.POST['type'] == 'district':
            target_district = request.POST["district"]
            images = []
            images.append(plot_bar_district_chart(target_district))
            images.append(plot_pie_district_chart(target_district))
            images.append(plot_bar_districtyear_chart(target_district))
            return render(request, "why.html", {"district": True, "images": images})
        if request.POST['type'] == 'district2':
            districts = []
            districts.append(request.POST["district1"])
            districts.append(request.POST["district2"])
            images = []
            images.append(plot_bar_districts_chart(districts))
            return render(request, "why.html", {"district": True, "images": images})
        if request.POST['type'] == 'state':
            target_district = request.POST["state"]
            images = []
            images.append(plot_bar_state_chart(target_district))
            images.append(plot_pie_state_chart(target_district))
            return render(request, "why.html", {"district": True, "images": images})
        
    return render(request, 'why.html')


def check_user_type(request):
    if request.method=="POST":
        if request.POST["user_type"]=="user":
            return redirect("/accounts/login")
        else:
            return redirect("user/police/login")
    return render(request, "account/check_user_type.html")

def check_user_type_signup(request):
    if request.method=="POST":
        if request.POST["user_type"]=="user":
            return redirect("/accounts/signup")
        else:
            return redirect("user/police/signup")
    return render(request, "account/check_user_type_signup.html")