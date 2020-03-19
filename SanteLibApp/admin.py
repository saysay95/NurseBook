from django.contrib import admin

# Register your models here.
from .models import Nurse
from .models import Patient
admin.site.register(Nurse)
admin.site.register(Patient)