from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): 

    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'), 
        ('patient', 'Patient'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    username = None 
    email = models.EmailField(unique=True, default='')
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['user_type'] 

   
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="core_users",  
        blank=True,
        help_text="The groups this user belongs to."
    )
    
   
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="core_users_permissions",
        blank=True
    )

    def __str__(self):
        return f"{self.get_full_name() or self.email} ({self.get_user_type_display()})"


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()  
    consultation_fee = models.PositiveIntegerField()
    availability = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
   
    def __str__(self):
        return f"Dr. {self.user.first_name} ({self.specialization})"

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    contact_info = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()  
    
    def __str__(self):
        return f"Patient: {self.user.first_name} - Age: {self.age}"

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  


    def __str__(self):
        return f"Appointment: Dr. {self.doctor.user.first_name} - {self.patient.user.first_name} - {self.date} - {self.time}"


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medications = models.TextField()
    notes = models.TextField()
    
   
    def __str__(self):
        return f"Prescription: Dr. {self.appointment.doctor.user.first_name} - {self.appointment.patient.user.first_name} - {self.appointment.date}"


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Chat: {self.sender.get_full_name()} -> {self.receiver.get_full_name()} at {self.timestamp}"
