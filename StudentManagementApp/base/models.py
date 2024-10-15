from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class User(AbstractUser):
    STATUSES = (('None', 'None'), ('Regular', 'Regular'), ('Part time', 'Part time'))
    status = models.CharField(max_length=50, choices=STATUSES, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)


class Subject(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    program = models.CharField(max_length=50, null=True, blank=True)
    ects = models.PositiveSmallIntegerField(null=True, blank=True)
    semester_regular = models.PositiveSmallIntegerField(null=True, blank=True)
    semester_part_time = models.PositiveSmallIntegerField(null=True, blank=True)
    MANDATORY = (('Yes', 'Yes'), ('No', 'No'))
    mandatory = models.CharField(max_length=50, choices=MANDATORY, null=True, blank=True)
    lecturer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

 
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, null=True, blank=True)
    STATUS = (('Not enrolled', 'Not enrolled'), ('Enrolled', 'Enrolled'), ('Passed', 'Passed'), ('Not passed', 'Not passed'))
    status = models.CharField(max_length=50, choices=STATUS, null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.student.username, self.subject.name)