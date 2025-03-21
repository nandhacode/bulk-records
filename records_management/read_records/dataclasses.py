from dataclasses import dataclass
from datetime import date

@dataclass
class EmployeeData:
    emp_id: str
    name: str
    email: str
    department: str
    designation: str
    salary: float
    date_of_joining: date
