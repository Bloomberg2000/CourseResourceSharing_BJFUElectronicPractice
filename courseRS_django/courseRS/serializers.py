import hashlib

from rest_framework import serializers
from courseRS.models import User, College, Course, SelectionLog


class UserSerializer(serializers.ModelSerializer):
    selectionLog = serializers.PrimaryKeyRelatedField(many=True, queryset=SelectionLog.objects.all())

    def create(self, validated_data):
        validated_data['password'] = md5(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.__contains__('password'):
            validated_data['password'] = md5(validated_data['password'])
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('pk', 'userName', 'email', 'phoneNum', 'userIDCard',
                  'password', 'school', 'college', 'subordinateClass', 'type',
                  'selectionLog')


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ('pk', 'name', 'offcialLink', 'logoLink')


class CourseSerializer(serializers.ModelSerializer):
    selectionLog = serializers.PrimaryKeyRelatedField(many=True, queryset=SelectionLog.objects.all())

    class Meta:
        model = Course
        fields = ('pk', 'name', 'subordinateSchoolAndCollege', 'checkInNum',
                  'currentStatus', 'info', 'link', 'selectionLog')


class SelectionLogSerializer(serializers.ModelSerializer):
    user_Name = serializers.ReadOnlyField(source='user.userName')
    selectedCourse_Name = serializers.ReadOnlyField(source='selectedCourse.name')

    def create(self, validated_data):
        # return validated_data
        return super().create(validated_data)

    class Meta:
        model = SelectionLog
        fields = ('pk', 'user', 'selectedCourse', 'time', 'user_Name', 'selectedCourse_Name', 'valid')


def md5(text):
    return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()
