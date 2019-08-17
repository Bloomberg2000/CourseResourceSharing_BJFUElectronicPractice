from rest_framework import generics
from rest_framework import permissions
from courseRS.models import User, College, Course, SelectionLog
from courseRS.serializers import UserSerializer, CollegeSerializer, CourseSerializer, SelectionLogSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CollegeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SelectionLogDetail(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CollegeList(generics.ListCreateAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SelectionLogList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
