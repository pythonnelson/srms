from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    residential_address = forms.CharField(widget=forms.Textarea, required=True)
    department = forms.ChoiceField(choices=Student.DEPARTMENT_CHOICES, required=True)
    faculty = forms.ChoiceField(choices=Student.FACULTY_CHOICES, required=True)
    program = forms.ChoiceField(choices=Student.PROGRAM_CHOICES, required=True)
    academic_level = forms.ChoiceField(choices=Student.ACADEMIC_LEVEL_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Applying Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name == 'residential_address':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Enter your residential address'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'required': True
                })
        
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username here'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create the Student record with all required fields
            Student.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                residential_address=self.cleaned_data['residential_address'],
                department=self.cleaned_data['department'],
                faculty=self.cleaned_data['faculty'],
                program=self.cleaned_data['program'],
                academic_level=self.cleaned_data['academic_level']
            )
        return user
    
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'residential_address',
            'department', 'faculty', 'program', 'academic_level',
            'profile_picture', 'cv'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'residential_address': forms.Textarea(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'academic_level': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_profile_picture(self):
        profile = self.cleaned_data.get('profile_picture')

        if profile:
            if profile.size > 5 * 1024 * 1024: # 5 MB
                raise forms.ValidationError("Image file is too large")
        return profile
        
    def clean_cv(self):
        cv = self.cleaned_data.get('cv')

        if cv:
            if cv.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size is too large')
        return cv