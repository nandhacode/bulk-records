from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CSVUploadForm
import csv
import pandas as pd
import requests, environ, os, json
from .models import Employee
from datetime import datetime, date
from django.urls import reverse

env = environ.Env()

environ.Env.read_env()

def Upload_employee(request):
    url = env('TOKEN_API_ENDPOINT')
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "username": env('TOKEN_USERNAME'),
        "password": env('TOKEN_PASSWORD')
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            
            if response_data['access']:
                os.environ['ACCESS_TOKEN'] = response_data['access']
            else:
                return HttpResponse(f'Token not generated, Status Code : {response.status_code}')
            
            return redirect(reverse('scv_file'))
        else:
            return HttpResponse(f'Failed to call API, Status Code : {response.status_code}')

    except requests.exceptions.RequestException as e:
        return HttpResponse(f'{e}')

def handle_csv_upload(request):
    form = CSVUploadForm()
    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            message = 'Only accept the CSV file format'
            return call_form(request,message)

        df = pd.read_csv(csv_file)
        df = df.dropna(axis=0, how='any')
        header_mapping = {
                'Employee ID': 'emp_id',
                'Name': 'name',
                'Email': 'email',
                'Department': 'department',
                'Designation': 'designation',
                'Salary': 'salary',
                'Date of Joining': 'date_of_joining',
            }
        if all(k in df.columns for k in ["Employee ID", "Name", "Email", "Department", "Designation", "Salary", "Date of Joining"]):
            df = df.rename(columns=header_mapping)
            df = df.drop_duplicates(subset=['emp_id'], keep='first')
            df = df.drop_duplicates(subset=['email'], keep='first')
        else:
            message = "The CSV file columns must have 'Employee ID', 'Name', 'Email', 'Department', 'Designation', 'Salary', 'Date of Joining'."
            return call_form(request,message)
        json_data = df.to_dict(orient='records')
        
        existing_emp_ids = list(Employee.objects.values_list('emp_id', flat=True))
        existing_emp_emails = list(Employee.objects.values_list('email', flat=True))
        
        try:
            non_existing_records = [ 
            {
                'emp_id': str(int(record['emp_id'])),
                'name': record['name'],
                'email': record['email'],
                'department': record['department'],
                'designation': record['designation'],
                'salary': record['salary'],
                'date_of_joining': datetime.strptime(record['date_of_joining'], '%d-%m-%Y').strftime('%Y-%m-%d')
            }
            for record in json_data 
            if str(record['emp_id']) not in existing_emp_ids and record['email'] not in existing_emp_emails]
        except Exception as e:
            message = 'Please check the column format'
            return call_form(request,message)

        url = env('ADD_EMPLOYEE_DETAILS_ENDPOINT')
        headers = {
            "Authorization": f"Bearer {env('ACCESS_TOKEN')}",
            "Content-Type": "application/json",
        }
        data = {
            "employees" : non_existing_records
        }

        try:
            if env('ACCESS_TOKEN'):
                if not len(non_existing_records):
                    message = "All employee data's are existing from DB, Please upload the new employee details"
                    return call_form(request,message)
                response = requests.post(url, json=data, headers=headers)
                response_data = response.json()

                if response.status_code == 200 | response.status_code == 201:
                    return call_form(request,response_data["message"])
                else:
                    return call_form(request,response_data["message"])
            else:
                message = "Please create the Access Token, Token is missing"
                return call_form(request,message)
        except requests.exceptions.RequestException as e:
            return call_form(request,e)
    else:
        message = ''
        return call_form(request,message)


def call_form(request,message):
    form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form,'message':message})            