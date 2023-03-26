import uuid
from django.db import models


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255) 
    designation = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    pic_url = models.TextField()

    client_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    hair_color = models.CharField(max_length=255)
    eye_color = models.CharField(max_length=255)
    height = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)

    firm_name = models.CharField(max_length=255)
    firm_location = models.CharField(max_length=255)

    birthdate = models.DateField()

    # employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Box(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    box_number = models.CharField(max_length=255)
    size = models.CharField(max_length=20)
    available = models.BooleanField()

    def __str__(self):
        return self.box_number



class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    registration_date = models.DateField()
    rental_duration = models.IntegerField()
    billing_amount = models.FloatField()
    islast = models.BooleanField()

    def __str__(self):
        return f"{self.box.box_number} - {self.client.name} ({self.registration_date})"

    
    
class Visitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    visit_date = models.DateField()
    check_in = models.TimeField()
    check_out = models.TimeField()

    def __str__(self):
        return f"{self.box.box_number} - {self.client.name} ({self.visit_date})"
