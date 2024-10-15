from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .decorators import *
from .models import *
from .forms import *

# Create your views here.

@login_required(login_url="/login/")
def index_page(request):
    user = request.user
    return render(request, "index.html", {"user":user})

@login_required(login_url="/login/")
def get_all_subjects(request):
    subjects = Subject.objects.all()
    return render(request, "all_subjects.html", {"subjects":subjects})

@login_required(login_url="/login/")
def get_subject(request, id):
    subject = Subject.objects.get(pk=id)
    return render(request, "subject_details.html", {"subject":subject})

@login_required(login_url="/login/")
@admin_only
def edit_subject(request, id):
    subject = Subject.objects.get(pk=id)
    if request.method == "GET":
        form = SubjectForm(instance=subject)
        return render(request, "edit_subject.html", {"form":form})
    elif request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("subjects")
        else:
            return HttpResponse("<h3> Unable to edit subject </h3>")
    else:
        return HttpResponseNotAllowed("<h3> Unable to edit subject </h3>")

@login_required(login_url="/login/")
@admin_only   
def add_subject(request):
    if request.method == "GET":
        form = SubjectForm()
        return render(request, "add_subject.html", {"form":form})
    elif request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subjects")
        else:
            return HttpResponse("<h3> Unable to add subject </h3>")
    else:
        return HttpResponseNotAllowed("<h3> Unable to add subject </h3>")

@login_required(login_url="/login/")
@admin_only
def delete_subject(request, id):
    subject = Subject.objects.get(pk=id)
    if request.method == "GET":
        return render(request, "delete_subject.html", {"subject":subject})
    elif request.method == "POST":
        if "delete_confirm" in request.POST:
            subject.delete()
        return redirect("subjects")
    else:
        return HttpResponseNotAllowed("<h3> Unable to delete subject </h3>")
    
#########################################################################################

@login_required(login_url="/login/")
def get_all_professors(request):
    role_professor = Role.objects.get(name="Professor")
    professors = User.objects.filter(role=role_professor)
    return render(request, "all_professors.html", {"professors":professors})

@login_required(login_url="/login/")
@admin_only
def add_professor(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "add_professor.html", {"form":form})
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("all_professors")
        else:
            return HttpResponse("<h3> Unable to add professor </h3>")
    else:
            return HttpResponse("<h3> Unable to add professor </h3>")

def get_user(request, id):
        user = User.objects.get(pk=id)
        return render(request, "user_details.html", {"user":user})

@login_required(login_url="/login/")
@admin_only
def edit_user(request, id):
    user = User.objects.get(pk=id)
    user_role = user.role.name
    if request.method == "GET":
        form = EditUserForm(instance=user)
        return render(request, "edit_user.html", {"form":form, "user":user})
    elif request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user_role == "Professor":
                return redirect('all_professors')
            elif user_role == "Student":
                return redirect('all_students')
        else:
            return HttpResponse("<h3> Unable to edit user </h3>")
    else:
        return HttpResponse("<h3> Unable to edit user </h3>")

@login_required(login_url="/login/")
@admin_only
def delete_user(request, id):
    user = User.objects.get(pk=id)
    user_role = user.role.name
    if request.method == "GET":
        return render(request, "delete_user.html", {"user":user})
    elif request.method == "POST":
        if "confirm_delete" in request.POST:
            user.delete()
            if user_role == "Professor":
                return redirect('all_professors')
            elif user_role == "Student":
                return redirect == ('all_students')
        elif "abort_delete" in request.POST:
            pass
        return redirect("user_details", id)

#########################################################################################

@login_required(login_url="/login/")
def get_all_students(request):
    student_role = Role.objects.get(name="Student")
    students = User.objects.filter(role=student_role)
    return render(request, "all_students.html", {"students":students})

@login_required(login_url="/login/")
@admin_only
def add_student(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "add_student.html", {"form":form})
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            student = form.save()
            subjects = Subject.objects.all()
            for subject in subjects:
                enrollment = Enrollment(student=student, subject=subject, status="Not enrolled")
                enrollment.save()
            return redirect('all_students')
        else:
            return HttpResponse("<h3> Unable to add student </h3>")
    else:
        return HttpResponse("<h3> Unable to add student </h3>")


@login_required(login_url="/login/")
@admin_only
def student_enrollments(request, id):
    student = User.objects.get(pk=id)
    enrollments = Enrollment.objects.filter(student=student)
    args = {
        "student":student,
        "enrollments":enrollments,
        "regular_semesters": [1, 2, 3, 4, 5, 6],
        "part_time_semesters": [1, 2, 3, 4, 5, 6, 7, 8]
    }

    return render(request, "student_enrollments.html", args)


@login_required(login_url="/login/")

def change_subject_status(request, id, new_status):
    enrollment = Enrollment.objects.get(pk=id)
    if request.method == "GET":
        return render(request, "update_enrollment_status.html", {"enrollment":enrollment, "new_status":new_status})
    
    elif request.method == "POST":
        if new_status == "Enrolled":
            student_enrollments = Enrollment.objects.filter(student=enrollment.student)
            can_enroll = True
            if enrollment.student.status == "Regular":
                if enrollment.subject.semester_regular in [3, 4]:
                    for student_enrollment in student_enrollments:
                        if student_enrollment.subject.semester_regular in [1, 2] and student_enrollment.status != "Passed":
                            can_enroll = False
                            break
                
                elif enrollment.subject.semester_regular in [5, 6]:
                    for student_enrollment in student_enrollments:
                        if student_enrollment.subject.semester_regular in [1, 2, 3, 4] and student_enrollment.status != "Passed":
                            can_enroll = False
                            break
                
            elif enrollment.student.status == "Part time":
                if enrollment.subject.semester_part_time in [3, 4]:
                    for student_enrollment in student_enrollments:
                        if student_enrollment.subject.semester_part_time in [1, 2] and student_enrollment.status != "Passed":
                            can_enroll = False
                            break
                
                elif enrollment.subject.semester_part_time in [5, 6]:
                    for student_enrollment in student_enrollments:
                        if student_enrollment.subject.semester_part_time in [1, 2, 3, 4] and student_enrollment.status != "Passed":
                            can_enroll = False
                            break
                
                elif enrollment.subject.semester_part_time in [7, 8]:
                    for student_enrollment in student_enrollments:
                        if student_enrollment.subject.semester_part_time in [1, 2, 3, 4, 5, 6] and student_enrollment.status != "Passed":
                            can_enroll = False
                            break

            if can_enroll == False:
                return HttpResponse("<h4> Student can't enroll on this subject until all subjects from previous years have been passed.")
            

        if "Yes" in request.POST:
            enrollment.status = new_status
            enrollment.save()

        if request.user.role.name == "Student":
            return redirect("my_student_enrollments")
        elif request.user.role.name == "Professor":
            return redirect("subject_enrollments", enrollment.subject.id)
        elif request.user.role.name == "Administrator":
            return redirect("student_enrollments", enrollment.student.id)

    else:
        return HttpResponse("<h4> Not possible to change status </h4>")


@login_required(login_url="/login/")
@admin_and_professor_only
def get_subject_enrollments(request, id):
     subject = Subject.objects.get(pk=id)
     enrollments = Enrollment.objects.filter(subject=subject)
     return render(request, "subject_enrollments.html", {"enrollments":enrollments, "subject":subject})

@login_required(login_url="/login/")
@professor_only
def get_subjects_by_professor(request):
    professor = request.user
    subjects = Subject.objects.filter(lecturer=professor)
    return render(request, "subjects_by_professor.html", {"subjects":subjects, "professor":professor})


@login_required(login_url="/login/")
@professor_only
def get_subjects_by_professor_and_status(request, status, id):
    subject = Subject.objects.get(pk=id)
    enrollments = Enrollment.objects.filter(status=status, subject=subject)
    
    return render(request, "subject_enrollments.html", {"enrollments":enrollments, "subject":subject})



@login_required(login_url="/login/")
@student_only
def my_student_enrollments(request):
    student = request.user
    enrollments = Enrollment.objects.filter(student=student)
    args = {
        "student":student,
        "enrollments":enrollments,
        "regular_semesters": [1, 2, 3, 4, 5, 6],
        "part_time_semesters": [1, 2, 3, 4, 5, 6, 7, 8]
    }

    return render(request, "my_student_enrollments.html", args)

@login_required(login_url="/login/")
def students_over_30_ects(request):
    students = User.objects.filter(role__name="Student")
    students_list = []
    
    for student in students:
        enrollments = Enrollment.objects.filter(student=student, status="Enrolled")
        total_ects = sum(enrollment.subject.ects for enrollment in enrollments)
        
        if total_ects > 30:
            students_list.append({
                'student': student,
                'total_ects': total_ects
            })

    return render(request, "students_over_30_ects.html", {"students_list": students_list})


@login_required(login_url="/login/")
def get_all_students_by_status(request, status):
    student_role = Role.objects.get(name="Student")
    students = User.objects.filter(role=student_role, status=status)

    return render(request, "students_by_status.html", {"students":students})


# @login_required(login_url="/login/")
# @admin_only
# def students_passed_over_10_ects(request):
#     students = User.objects.filter(role__name="Student")
#     qualifying_students = 0
    
#     for student in students:
#         enrollments = Enrollment.objects.filter(student=student, status="Passed")
#         total_ects = sum(enrollment.subject.ects for enrollment in enrollments)
        
#         if total_ects > 10:
#             qualifying_students += 1

#     return render(request, "students_passed_over_10_ects.html", {"qualifying_students": qualifying_students})



@login_required(login_url="/login/")
@admin_only
def students_passed_over_10_ects(request):
    students = User.objects.filter(role__name="Student")
    qualifying_students = 0
    
    for student in students:
        enrollments = Enrollment.objects.filter(student=student, status="Passed")
        total_ects = sum(enrollment.subject.ects for enrollment in enrollments)
        
        if total_ects > 10:
            qualifying_students += 1

    return render(request, "students_passed_over_10_ects.html", {"qualifying_students": qualifying_students})


@login_required(login_url="/login/")
@admin_only
def students_details_over_10_ects(request):
    students = User.objects.filter(role__name="Student")
    qualifying_students = []

    for student in students:
        enrollments = Enrollment.objects.filter(student=student, status="Passed")
        total_ects = sum(enrollment.subject.ects for enrollment in enrollments)
        
        if total_ects > 10:
            qualifying_students.append(student)

    return render(request, "students_details_over_10_ects.html", {"qualifying_students": qualifying_students})
