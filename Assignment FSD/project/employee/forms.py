from django import forms
from django.core.exceptions import ValidationError

class EmployeeDetails(forms.Form):
    f_name = forms.CharField(
        max_length=75,
        min_length=3,
        required=True,
        label= "Employee Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'employee-name',
        })
    )

    
    f_email = forms.EmailField(
        required=True,
        label="Employee Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@domain.com', 
            'class': 'form-control', 
            'id':'employee-email'
        })
    )

    f_mobile = forms.CharField(
        max_length=10,
        required=True,
        label='Mobile No',
        widget=forms.TextInput(attrs={
            'placeholder': '7896451236',
            'class': 'form-control',
            'id': 'employee-number'
        })
    )

    designations = [
        ("hr", "HR"),
        ("manager", "Manager"),
        ("sales", "Sales"),
    ]

    f_designation = forms.ChoiceField(
        label="Designation",
        choices=designations,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'employee-designation'
        })
    )

    gender = [
        ('male', 'Male'),
        ('female', "Female")
    ]

    f_gender = forms.ChoiceField(
        label="Gender",
        required=True,
        choices=gender,
        widget = forms.RadioSelect(attrs={
            'class': 'form-control',
            'id': 'employee-gender'
        })
    )

    courses = [
        ("mca", "MCA"),
        ("bca", "BCA"),
        ("bsc", "BSC"),
    ]

    f_course = forms.MultipleChoiceField(
        label="Course",
        required=True,
        choices=courses,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'employee-course'
        })
    )

    f_createDate = forms.DateField(
        label="Date",
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'createDate'
        })
    )

    f_image = forms.ImageField(
        label="Image Upload",
        required=True,
    )

    def clean_f_image(self):
        image = self.cleaned_data.get('f_image')
        
        if image:
            if not image.name.lower().endswith(('jpg', 'jpeg', 'png')):
                raise ValidationError("Only JPG and PNG files are allowed.")
        return image