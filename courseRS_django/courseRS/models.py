from django.db import models


# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phoneNum = models.CharField(max_length=11, unique=True)
    userIDCard = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    subordinateClass = models.CharField(max_length=100,null=True ,blank=True)
    type = models.IntegerField(default=0)


class College(models.Model):
    name = models.CharField(max_length=100, unique=True)
    offcialLink = models.CharField(max_length=1000)
    logoLink = models.CharField(max_length=1000)


class Course(models.Model):
    name = models.CharField(max_length=100)
    subordinateSchoolAndCollege = models.CharField(max_length=100)
    currentStatus = models.CharField(max_length=100)
    checkInNum = models.IntegerField()
    info = models.CharField(max_length=100)
    link = models.CharField(max_length=1000, default='')


class SelectionLog(models.Model):
    user = models.ForeignKey("User", related_name='selectionLog', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    selectedCourse = models.ForeignKey("Course", related_name='selectionLog', on_delete=models.CASCADE)
    valid = models.BooleanField(default=True)
