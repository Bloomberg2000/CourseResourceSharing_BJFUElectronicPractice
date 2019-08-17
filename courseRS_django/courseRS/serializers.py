from rest_framework import serializers
from courseRS.models import User, College, Course, SelectionLog


class UserSerializer(serializers.ModelSerializer):
    selectionLog = serializers.PrimaryKeyRelatedField(many=True, queryset=SelectionLog.objects.all())

    class Meta:
        model = User
        fields = ('userName', 'stuCode', 'email', 'phoneNum',
                  'password', 'school', 'college', 'major', 'subordinateClass', 'selectionLog')


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ('name', 'offcialLink')


class CourseSerializer(serializers.ModelSerializer):
    selectionLog = serializers.PrimaryKeyRelatedField(many=True, queryset=SelectionLog.objects.all())

    class Meta:
        model = Course
        fields = ('name', 'subordinateSchoolAndCollege', 'openTime',
                  'period', 'info', 'link', 'selectionLog')


class SelectionLogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.userName')
    selectedCourse = serializers.ReadOnlyField(source='selectedCourse.name')

    class Meta:
        model = Course
        fields = ('user', 'selectedCourse', 'valid')
