from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm


def student_list(request):
    students = Student.objects.all().order_by('name')
    context = {
        'students': students,
    }
    return render(request, 'school/student_list.html', context)


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('school:student_list')
    else:
        form = StudentForm()

    context = {
        'form': form,
    }
    return render(request, 'school/student_form.html', context)


def student_update(request, pk: int):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('school:student_list')
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'student': student,
    }
    return render(request, 'school/student_form.html', context)


def student_delete(request, pk: int):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.delete()
        return redirect('school:student_list')

    context = {
        'student': student,
    }
    return render(request, 'school/student_confirm_delete.html', context)
