from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import *
from .models import *


# Create your views here.
def student_register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('students:student_login') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentRegistrationForm()
    
    context = {'form': form}
    return render(request, "students/register.html", context)

def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        
        if username and password:
            # Strip whitespace from username
            username = username.strip()
            
            user = authenticate(request, username=username, password=password)

            if user is not None:

                # Check if user is active
                if not user.is_active:
                    messages.error(request, "Your account has been deactivated.")
                    return render(request, "students/login.html")
                
                # Check if the user is a student
                if hasattr(user, 'student'):
                    try:
                        # Verify student profile exists and is accessible
                        # student_profile = user.student
                        login(request, user)
                        
                        # Handle "Remember Me" functionality
                        if remember_me == 'true': 
                            # Set session to expire in 2 weeks
                            request.session.set_expiry(1209600)  # 2 weeks in seconds
                        else:
                            # Set session to expire when browser closes
                            request.session.set_expiry(0)
                        messages.success(request, f"Welcome back, {user.username}!")
                        
                        # Check if there's a 'next' parameter for redirect
                        next_url = request.POST.get('next') or request.GET.get('next')
                        if next_url:
                            return redirect(next_url)
                        
                        return redirect('students:student_dashboard')
                        
                    except Exception as e:
                        messages.error(request, "Error accessing your student profile. Please contact administrator.")
                else:
                    messages.error(request, "You are not registered as a student.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please enter both username and password.")
    
    return render(request, "students/login.html")

@login_required
def student_dashboard(request):
    # Check if user is a student
    if not hasattr(request.user, 'student'):
        messages.error(request, "Access denied. Students only.")
        return redirect('students:student_login')
    
    context = {
        'student': request.user.student
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def student_profile(request):
    # Ensure user is a student
    if not hasattr(request.user, 'student'):
        raise HttpResponseForbidden("Access Denied")
    
    student = request.user.student

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('students:student_dashboard')
    else:
        form = StudentProfileForm(instance=student)
    context = {
        'form': form,
        'student': student
    }
    return render(request, 'students/profile.html', context)

def registrar_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        
        if username and password:
            # Strip whitespace from username
            username = username.strip()
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if user is active
                if not user.is_active:
                    messages.error(request, "Your account has been deactivated.")
                    return render(request, "registrar/login.html")

                # Check if the user is a registrar
                try:
                    registrar = Registrar.objects.get(user=user)
                    
                    login(request, user)
                    
                    # Handle "Remember Me" functionality
                    if remember_me == 'true': 
                        # Set session to expire in 2 weeks
                        request.session.set_expiry(1209600)  # 2 weeks in seconds
                    else:
                        # Set session to expire when browser closes
                        request.session.set_expiry(0)
                        
                    messages.success(request, f"Welcome back, {user.username}!")
                    
                    # Check if there's a 'next' parameter for redirect
                    next_url = request.POST.get('next') or request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    
                    return redirect('students:registrar_dashboard')
                    
                except Registrar.DoesNotExist:
                    messages.error(request, "You are not registered as a registrar.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please enter both username and password.")
    
    return render(request, "registrar/login.html")

@login_required
def registrar_dashboard(request):
    students = Student.objects.all()
    new_students_count = Student.objects.filter(
        created_at__month=timezone.now().month
    ).count()
    
    context = {
        'students': students,
        'new_students_count': new_students_count,
        'registrar': request.user.registrar,
    }
    return render(request, 'registrar/dashboard.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def delete_student(request, student_id):
    # Ensure user is a registrar
    try:
        registrar = Registrar.objects.get(user=request.user)
    except Registrar.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Access denied. Registrars only.'}, status=403)
        messages.error(request, "Access denied. Registrars only.")
        return redirect('students:registrar_login')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == "POST":
        try:
            # Store student name for success message
            student_name = f"{student.first_name} {student.last_name}"
            user = student.user
            
            # Delete student and associated user
            student.delete()
            user.delete()
            
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': f'Student {student_name} has been deleted successfully!'
                })
            
            # Handle regular form submission
            messages.success(request, f"Student {student_name} has been deleted successfully!")
            return redirect('students:registrar_dashboard')
            
        except Exception as e:
            # Handle any errors during deletion
            error_message = f"An error occurred while deleting the student: {str(e)}"
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'message': error_message
                }, status=500)
            
            messages.error(request, error_message)
            return redirect('students:registrar_dashboard')
    
    # If GET request, show confirmation page (for non-AJAX requests)
    context = {'student': student}
    return render(request, "registrar/confirm_delete.html", context)

@login_required
def student_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('students:student_login')