from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import FileExtensionValidator

# Create your models here.
class Student(models.Model):
    DEPARTMENT_CHOICES = [
        ('computer_science', 'Computer Science'),
        ('engineering', 'Engineering'),
        ('business_information', 'Business Information'),
        ('law', 'Law'),
        ('medicine', 'Medicine')
    ]

    FACULTY_CHOICES = [
        ('science', 'Faculty of Science'),
        ('engineering', 'Faculty of Engineering'),
        ('business', 'Faculty of Business')
    ]
    PROGRAM_CHOICES = [
        ('bachelor', "Bachelor\'s Degree"),
        ('master', "Master\'s Degree"),
        ('phd', "PhD"),
        ('diploma', "Diploma"),
    ]
    ACADEMIC_LEVEL_CHOICES = [
        ('year_1', "Year 1"),
        ('year_2', "Year 2"),
        ('year_3', "Year 3"),
        ('year_4', "Year 4"),
    ]
    #  1 -> 1 realtionship
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    residential_address = models.TextField()
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    faculty = models.CharField(max_length=100, choices=FACULTY_CHOICES)
    program = models.CharField(max_length=100, choices=PROGRAM_CHOICES)
    academic_level = models.CharField(max_length=100, choices=ACADEMIC_LEVEL_CHOICES)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )
    cv = models.FileField(
        upload_to="cvs/",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Registrar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Registrar: {self.user.username}"