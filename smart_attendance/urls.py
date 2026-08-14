from django.contrib import admin
from django.urls import path

from attendance import views


urlpatterns = [

    # =====================================================
    # ADMIN
    # =====================================================

    path(
        'admin/',
        admin.site.urls
    ),


    # =====================================================
    # LOGIN / LOGOUT
    # =====================================================

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        '',
        views.home,
        name='home'
    ),


    # =====================================================
    # STUDENTS
    # =====================================================

    path(
        'students/',
        views.student_list,
        name='student_list'
    ),

    path(
        'students/add/',
        views.add_student,
        name='add_student'
    ),

    path(
        'edit/<int:id>/',
        views.edit_student,
        name='edit_student'
    ),

    path(
        'delete/<int:id>/',
        views.delete_student,
        name='delete_student'
    ),


    # =====================================================
    # ATTENDANCE
    # =====================================================

    path(
        'attendance/',
        views.attendance_list,
        name='attendance_list'
    ),

    path(
        'mark/<int:id>/',
        views.mark_attendance,
        name='mark_attendance'
    ),


    # =====================================================
    # STUDENT ATTENDANCE
    # =====================================================

    path(
        'student-attendance/<int:id>/',
        views.student_attendance,
        name='student_attendance'
    ),


    # =====================================================
    # ATTENDANCE REPORT
    # =====================================================

    path(
        'attendance-report/',
        views.attendance_report,
        name='attendance_report'
    ),


    # =====================================================
    # DOWNLOAD CSV
    # =====================================================

    path(
        'attendance/download/',
        views.download_attendance,
        name='download_attendance'
    ),

]
