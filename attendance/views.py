from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import csv


from .models import Student, Attendance


# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        return render(
            request,
            'login.html',
            {
                'error': 'Invalid username or password'
            }
        )

    return render(
        request,
        'login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    return redirect('login')


# =========================================================
# HOME / DASHBOARD
# =========================================================

@login_required(login_url='login')
def home(request):

    total_students = Student.objects.count()

    today = timezone.localdate()

    today_attendance = Attendance.objects.filter(
        date=today
    )

    present_count = today_attendance.filter(
        status='Present'
    ).values(
        'student'
    ).distinct().count()

    absent_count = total_students - present_count

    if total_students > 0:

        attendance_percentage = round(
            (present_count / total_students) * 100,
            2
        )

    else:

        attendance_percentage = 0

    return render(
        request,
        'home.html',
        {
            'total_students': total_students,
            'present_count': present_count,
            'absent_count': absent_count,
            'attendance_percentage': attendance_percentage,
            'today': today,
        }
    )


# =========================================================
# STUDENT LIST + SEARCH
# =========================================================

@login_required(login_url='login')
def student_list(request):

    query = request.GET.get('q', '')

    if query:

        students = Student.objects.filter(

            Q(name__icontains=query) |
            Q(roll_no__icontains=query)

        )

    else:

        students = Student.objects.all()

    return render(
        request,
        'student_list.html',
        {
            'students': students,
            'query': query,
        }
    )


# =========================================================
# ADD STUDENT
# =========================================================

@login_required(login_url='login')
def add_student(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        email = request.POST.get('email')
        department = request.POST.get('department')

        Student.objects.create(

            name=name,
            roll_no=roll_no,
            email=email,
            department=department

        )

        return redirect('student_list')

    return render(
        request,
        'add_student.html'
    )


# =========================================================
# EDIT STUDENT
# =========================================================

@login_required(login_url='login')
def edit_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == 'POST':

        student.name = request.POST.get('name')
        student.roll_no = request.POST.get('roll_no')
        student.email = request.POST.get('email')
        student.department = request.POST.get('department')

        student.save()

        return redirect('student_list')

    return render(
        request,
        'edit_student.html',
        {
            'student': student
        }
    )


# =========================================================
# DELETE STUDENT
# =========================================================

@login_required(login_url='login')
def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    student.delete()

    return redirect('student_list')


# =========================================================
# ATTENDANCE LIST
# =========================================================

@login_required(login_url='login')
def attendance_list(request):

    selected_date = request.GET.get(
        'date',
        ''
    )

    if selected_date:

        attendances = Attendance.objects.select_related(
            'student'
        ).filter(
            date=selected_date
        ).order_by(
            '-date',
            '-time'
        )

    else:

        attendances = Attendance.objects.select_related(
            'student'
        ).order_by(
            '-date',
            '-time'
        )

    return render(
        request,
        'attendance_list.html',
        {
            'attendances': attendances,
            'selected_date': selected_date,
        }
    )


# =========================================================
# MARK ATTENDANCE MANUALLY
# =========================================================

@login_required(login_url='login')
def mark_attendance(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    today = timezone.localdate()

    already_marked = Attendance.objects.filter(
        student=student,
        date=today
    ).exists()

    if not already_marked:

        Attendance.objects.create(

            student=student,

            date=today,

            time=timezone.localtime().time(),

            status='Present'

        )

    return redirect(
        'attendance_list'
    )


# =========================================================
# STUDENT-WISE ATTENDANCE
# =========================================================

@login_required(login_url='login')
def student_attendance(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by(
        '-date',
        '-time'
    )

    # Total unique attendance dates
    total_classes = Attendance.objects.values(
        'date'
    ).distinct().count()

    # Student's present days
    present_days = attendance_records.filter(
        status='Present'
    ).values(
        'date'
    ).distinct().count()

    # Absent days
    absent_days = total_classes - present_days

    if absent_days < 0:

        absent_days = 0

    # Percentage
    if total_classes > 0:

        attendance_percentage = round(
            (present_days / total_classes) * 100,
            2
        )

    else:

        attendance_percentage = 0

    # Status
    if attendance_percentage >= 75:

        attendance_status = 'Good Attendance'

    else:

        attendance_status = 'Low Attendance'

    return render(
        request,
        'student_attendance.html',
        {
            'student': student,
            'attendance_records': attendance_records,
            'total_classes': total_classes,
            'present_days': present_days,
            'absent_days': absent_days,
            'attendance_percentage': attendance_percentage,
            'attendance_status': attendance_status,
        }
    )


# =========================================================
# ALL STUDENTS ATTENDANCE REPORT
# =========================================================

@login_required(login_url='login')
def attendance_report(request):

    students = Student.objects.all()

    # Total number of unique attendance dates
    total_classes = Attendance.objects.values(
        'date'
    ).distinct().count()

    student_reports = []

    for student in students:

        present_days = Attendance.objects.filter(

            student=student,

            status='Present'

        ).values(
            'date'
        ).distinct().count()

        absent_days = total_classes - present_days

        if absent_days < 0:

            absent_days = 0

        if total_classes > 0:

            percentage = round(

                (present_days / total_classes) * 100,

                2

            )

        else:

            percentage = 0

        if percentage >= 75:

            status = 'Good Attendance'

        else:

            status = 'Low Attendance'

        student_reports.append({

            'student': student,

            'total_classes': total_classes,

            'present_days': present_days,

            'absent_days': absent_days,

            'percentage': percentage,

            'status': status,

        })

    return render(
        request,
        'attendance_report.html',
        {
            'student_reports': student_reports,
            'total_classes': total_classes,
        }
    )


# =========================================================
# DOWNLOAD ATTENDANCE CSV
# =========================================================

@login_required(login_url='login')
def download_attendance(request):

    selected_date = request.GET.get(
        'date',
        ''
    )

    if selected_date:

        attendances = Attendance.objects.select_related(
            'student'
        ).filter(
            date=selected_date
        ).order_by(
            'date',
            'time'
        )

    else:

        attendances = Attendance.objects.select_related(
            'student'
        ).order_by(
            'date',
            'time'
        )

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="attendance_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'ID',
        'Student Name',
        'Roll No',
        'Email',
        'Department',
        'Date',
        'Time',
        'Status'
    ])

    for attendance in attendances:

        student = attendance.student

        writer.writerow([

            student.id,

            student.name,

            student.roll_no,

            student.email,

            student.department,

            attendance.date,

            attendance.time,

            attendance.status

        ])

    return response
