import csv, json
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CSVUploadForm
from .models import Employee
from .dataclasses import EmployeeData
from .decorators import validate_employee_data, log_request
from django.db import IntegrityError

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

class RegisterUserView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        data = request.data
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @log_request
    @validate_employee_data
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except Exception as e:
            return Response({'JSON message': {e}}, status=404)

        try:
            employees_data = [
                EmployeeData(
                    emp_id=employee['emp_id'],
                    name=employee['name'],
                    email=employee['email'],
                    department=employee['department'],
                    designation=employee['designation'],
                    salary=employee['salary'],
                    date_of_joining=employee['date_of_joining']
                )
                for employee in data['employees']
            ]

            employee_instances = [
                Employee(
                    emp_id=emp_data.emp_id,
                    name=emp_data.name,
                    email=emp_data.email,
                    department=emp_data.department,
                    designation=emp_data.designation,
                    salary=emp_data.salary,
                    date_of_joining=emp_data.date_of_joining
                )
                for emp_data in employees_data
            ]
        except Exception as e:
            return Response({'Data class error handling': {e}}, status=404)

        try:
            Employee.objects.bulk_create(employee_instances)
            return Response({'message': 'Employees data created successfully!','employees':data['employees']}, status=201)
        except Exception as e:
            return Response({'message': {e}}, status=404)    
    
class DeleteAllEmployeeData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            Employee.objects.all().delete()
        except Exception as e:
            return Response({'message': f'Something went wrong : {e}'}, status=400)
        return Response({'message': 'All Employees data has deleted successfully!'}, status=200)