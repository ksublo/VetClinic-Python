import datetime

from django.contrib.auth.models import User
from django.db import models


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.specialization}"


class Shift(models.Model):
    WEEKDAYS_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=WEEKDAYS_CHOICES, default='Monday')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name} - {self.day} - {self.start_time} - {self.end_time}"


class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Pet(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Not Known')
    ]
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='N')
    owner = models.ForeignKey(Host, related_name='pets', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.owner.user.first_name} {self.owner.user.last_name})"


class Illness(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    duration = models.DurationField(default=datetime.timedelta(minutes=30))
    medicines = models.ForeignKey('Medicine', on_delete=models.CASCADE, blank=True, null=True)
    illness = models.ForeignKey(Illness, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"({self.pet}) - ({self.doctor}) - ({self.date_time})"

