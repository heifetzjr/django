# Register your models here.
from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'birth_date', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('birth_date', 'created_at')
