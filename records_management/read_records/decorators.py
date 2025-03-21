# decorators.py
import logging
import json
from django.http import JsonResponse
# from datetime import datetime
# from functools import wraps

# logger = logging.getLogger(__name__)
# Logging Decorator
def log_request(func):
    def wrapper(self, request, *args, **kwargs):
        logging.info(f"Request Method: {request.method}")
        logging.info(f"Request Body: {request.body.decode('utf-8')}")
        response = func(self, request, *args, **kwargs)
        return response
    return wrapper

# Validation Decorator
def validate_employee_data(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            
            data = json.loads(request.body)
            # Ensure 'employees' key exists in the data
            if 'employees' not in data:
                return JsonResponse({"error": "'employees' key is required."}, status=400)

            employees = data['employees']

            # Ensure 'employees' is a list
            if not isinstance(employees, list):
                return JsonResponse({"error": "'employees' must be a list."}, status=400)
            
            # Validate each employee entry
            for employee in employees:
                if not all(k in employee for k in ["emp_id", "name", "email", "department", "designation", "salary", "date_of_joining"]):
                    return JsonResponse({"error": "Each employee must have 'emp_id', 'name', 'email', 'department', 'designation', 'salary', 'date_of_joining'."}, status=400)

                # Further validation can be done here (e.g., type checks, format checks)
                if not isinstance(employee["emp_id"], str):
                    return JsonResponse({"error": "emp_id must be a string."}, status=400)
                if not isinstance(employee["salary"], (int, float)):
                    return JsonResponse({"error": "salary must be a number."}, status=400)
                
            # If validation passes, proceed with the view
            return func(self, request, *args, **kwargs)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
    return wrapper
