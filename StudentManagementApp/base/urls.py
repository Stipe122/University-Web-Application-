from django.urls import path
from base import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('index/', views.index_page, name='index'),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('subjects/', views.get_all_subjects, name='subjects'),
    path('subjects/details/<int:id>', views.get_subject, name='subject_details'),
    path('subjects/edit/<int:id>', views.edit_subject, name='edit_subject'),
    path('subjects/add', views.add_subject, name='add_subject'),
    path('subjects/delete/<int:id>', views.delete_subject, name='delete_subject'),
    path('subjects/enrollments/<int:id>', views.get_subject_enrollments, name='subject_enrollments'),
    path('subjects/enrollments/<int:id>/<str:status>', views.get_subjects_by_professor_and_status, name='subjects_by_professor_and_status'),

    path('professors/', views.get_all_professors, name='all_professors'),
    path('professors/add', views.add_professor, name='add_professor'),
    path('users/<int:id>', views.get_user, name='user_details'),
    path('users/edit/<int:id>', views.edit_user, name='edit_user'),
    path('users/delete/<int:id>', views.delete_user, name='delete_user'),

    path('users/subject_by_professor/', views.get_subjects_by_professor, name='subjects_by_professor'),

    path('students/', views.get_all_students, name='all_students'),
    path('students/add', views.add_student, name='add_student'),

    path('students/enrollments/<int:id>', views.student_enrollments, name='student_enrollments'),
    path('student/enrollments/<int:id>/update/<str:new_status>', views.change_subject_status, name='update_enrollment_status'),
    path('students/my_enrollments/', views.my_student_enrollments, name='my_student_enrollments'),

    path('students/over_30_ects', views.students_over_30_ects, name='students_over_30_ects'),
    path('students/students_by_status/<str:status>', views.get_all_students_by_status, name='students_by_status'),

    path('students/students_passed_over_10_ects/', views.students_passed_over_10_ects, name='students_passed_over_10_ects'),

    path('students/students_details_over_10_ects/', views.students_details_over_10_ects, name='students_details_over_10_ects'),

]