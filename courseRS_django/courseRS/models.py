from django.db import models


# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=100)
    stuCode = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    phoneNum = models.CharField(max_length=11)
    password = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    subordinateClass = models.CharField(max_length=100)


class College(models.Model):
    name = models.CharField(max_length=100)
    offcialLink = models.CharField(max_length=1000)


class Course(models.Model):
    name = models.CharField(max_length=100)
    subordinateSchoolAndCollege = models.CharField(max_length=100)
    openTime = models.DateTimeField()
    period = models.IntegerField()
    info = models.CharField(max_length=100)
    link = models.CharField(max_length=1000, default='')


class SelectionLog(models.Model):
    user = models.ForeignKey("User", related_name='selectionLog', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    selectedCourse = models.ForeignKey("Course", related_name='selectionLog', on_delete=models.CASCADE)
    valid = models.BooleanField(default=True)
