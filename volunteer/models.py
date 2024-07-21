from django.db import models

class Volunteer(models.Model):

    gender_options = (
        ('female', 'female'),
        ('male', 'male')
    )
    name = models.CharField(max_length = 20, null = True, blank = True)
    age = models.IntegerField(null =True, blank = True)
    gender = models.CharField(max_length=20, null =True, blank =True, choices = gender_options)
    speciality = models.TextField(max_length = 200, null = True, blank = True)
    phone_number = models.CharField(max_length = 20, null = True, blank = True)
    years_of_volunteering_experience = models.IntegerField(null =True, blank = True)
    skills = models.TextField(max_length = 200, null = True, blank = True)
