from django.shortcuts import render, redirect
from .models import *
from .forms import EmployeeDetails
import re, os
from django.core.exceptions import ValidationError
from django.http import JsonResponse, Http404
from django.conf import settings
from django.contrib import messages


# This is used to Validate the Email.
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValidationError("Invalid email format.")


# This function is used to check whether the email or number is duplicate or not.
def check_duplicate_email_number(email, number):
    existing_employee = t_employee.find_one({"f_email": email})
    existing_number = t_employee.find_one({'f_mobile': number})
    if existing_employee:
        raise ValidationError("Email already exists. Please use a different email.")
    elif existing_number:
        raise ValidationError("Number already exists. Please use a different number.")


# Used for validating the phone number.
def validate_mobile_number(mobile_number):
    if not mobile_number.isdigit() or len(mobile_number) != 10:
        raise ValidationError("Invalid mobile number. It must be a 10-digit number.")


# Function is used to create a employee.
def create_employee(request):
    form = EmployeeDetails()

    if request.method == "POST":
        form = EmployeeDetails(request.POST, request.FILES)

        if form.is_valid():
            email = form.cleaned_data['f_email']
            mobile = form.cleaned_data['f_mobile']

            try:
                validate_email(email)
                validate_mobile_number(mobile)
                check_duplicate_email_number(email, mobile)
            except ValidationError as err:
                return JsonResponse({'success': False, 'errors': str(err)}) 

            max_f_no = t_employee.find_one(sort=[("f_no", -1)])
            next_f_no = (max_f_no['f_no'] + 1) if max_f_no else 1

            image = form.cleaned_data.get('f_image')
            image_path = ''

            if image:
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                image_path = os.path.join('employee_images', image.name)
                full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

            employee_data = {
                'f_no': next_f_no,
                "f_name": form.cleaned_data['f_name'],
                "f_email": form.cleaned_data['f_email'],
                "f_mobile": form.cleaned_data['f_mobile'],
                "f_designation": form.cleaned_data['f_designation'],
                "f_gender": form.cleaned_data['f_gender'],
                "f_course": form.cleaned_data['f_course'],
                "f_createDate": form.cleaned_data['f_createDate'].isoformat(),
                "f_image": os.path.join(settings.MEDIA_URL, image_path) if image_path else ''
            }

            t_employee.insert_one(employee_data)
            messages.success(request, 'Employee created successfully!')
            return redirect("show_employee")
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{field}: {error.as_text()}")

    context = {
        'form': form,
    }

    return render(request, "employee/create_emp.html", context)

# Simple Home Page
def home(request):
    return render(request, "employee/home.html")


# This function is used to Show employees 
def show_employees(request):
    query = request.GET.get('q', '')
    total_count = t_employee.count_documents({})

    if query:
        employees = list(t_employee.find(
            {"f_name": {"$regex": query, "$options": "i"}}
        ))
        search_count = len(employees)
    else:
        employees = list(t_employee.find())
        search_count = len(employees)

    context = {
        'employees': employees,
        'query': query,
        'total_count': total_count,
        'search_count': search_count,
        'MEDIA_URL': settings.MEDIA_URL
    }

    return render(request, "employee/employee_list.html", context)


# This function is used to edit the Existing document:
def edit_employees(request, f_no):
    employee = t_employee.find_one({'f_no': f_no})
    if not employee:
        raise Http404("Employee not found")
    
    if request.method == "POST":
        form = EmployeeDetails(request.POST, request.FILES)

        if form.is_valid():
            employee_data = {
                "f_name": form.cleaned_data['f_name'],
                "f_email": form.cleaned_data['f_email'],
                "f_mobile": form.cleaned_data['f_mobile'],
                "f_designation": form.cleaned_data['f_designation'],
                "f_gender": form.cleaned_data['f_gender'],
                "f_course": form.cleaned_data['f_course'],
                "f_createDate": form.cleaned_data['f_createDate'].isoformat(),
            }

            if 'f_image' in request.FILES:
                image = request.FILES['f_image']
                image_path = os.path.join('employee_images', image.name)
                full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                employee_data['f_image'] = os.path.join(settings.MEDIA_URL, image_path)


            t_employee.update_one({'f_no': f_no}, {'$set': employee_data})
            messages.success(request, 'Employee details updated successfully!')
            return redirect('show_employee')
        
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{field}: {error.as_text()}")
        
    else:
        initial_data = {
            'f_name': employee['f_name'],
            'f_email': employee['f_email'],
            'f_mobile': employee['f_mobile'],
            'f_designation': employee['f_designation'],
            'f_gender': employee['f_gender'],
            'f_course': employee['f_course'],
            'f_createDate': employee['f_createDate'],
            'f_image': employee.get('f_image', '')
        }
        form = EmployeeDetails(initial=initial_data)

    context = {
        'form': form,
        'employee': employee
    }

    return render(request, "employee/edit_emp.html", context)


# This function is used to Delete an existing employee
def delete_employee(request, f_no):
    try:
        employee = t_employee.find_one({'f_no': f_no})

        if not employee:
            raise Http404("Employee not found")

        t_employee.delete_one({'f_no': f_no})
        messages.success(request, 'Employee details deleted successfully!')
        return redirect('show_employee')

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})