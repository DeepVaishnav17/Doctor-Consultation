from django.contrib import admin
from .models import Doctor, Patient, User, Appointment, Prescription, Chat

# Register your models here.
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Chat)
