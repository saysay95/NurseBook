from django.db import models
import datetime
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
# Create your models here.

from SanteLib import config


class Address(models.Model):

    street = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30, blank=True, null=True)
    zip_code = models.PositiveIntegerField()


class Person(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField('Date of birth')
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    sex = models.CharField(choices=config.SEX_CHOICES,default='F',max_length=1)
    email = models.EmailField()

    def __str__(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize()

    def age(self):
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year

        if today < datetime.date(today.year, self.date_of_birth.month, self.date_of_birth.day):
            age -= 1

        return age

class Nurse(Person):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_graduation = models.DateField('Date of graduation')
    spoken_languages = MultiSelectField(max_choices=5, choices=config.LANGUAGE_CHOICES, default='FR')
    rating = models.PositiveIntegerField(choices=config.RATING_CHOICES, default=0)
    photo = models.ImageField(upload_to="photos/",null=True)
    diploma = models.FileField(upload_to="diplomas/",null=True)

    @property
    def photo_thumbnail(self):
        return self.photo.name.replace('photos','photos/small')

    def __str__(self):
        return self.user.username


class Patient(Person):

    preferred_languages = MultiSelectField(choices=config.LANGUAGE_CHOICES, max_length=3, default='FR')

    def __str__(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize()