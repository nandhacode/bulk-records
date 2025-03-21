from django.db import models

# Create your models here.
class Employee(models.Model):
    emp_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100,default='')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_joining = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.emp_id} - {self.email}'
    class Meta:
        db_table = 'read_records_employee'