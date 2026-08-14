from django.contrib import admin
from .models import Student, Attendance


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'roll_no',
        'email',
        'department',
    )

    search_fields = (
        'name',
        'roll_no',
        'email',
        'department',
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'date',
        'time',
        'status',
    )

    list_filter = (
        'date',
        'status',
    )

    search_fields = (
        'student__name',
        'student__roll_no',
    )
