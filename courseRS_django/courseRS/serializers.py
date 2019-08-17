import hashlib

from rest_framework import serializers
from courseRS.models import User, College, Course, SelectionLog


class UserSerializer(serializers.ModelSerializer):
    selectionLog = serializers.PrimaryKeyRelatedField(many=True, queryset=SelectionLog.objects.all())

    class Meta:
        model = User
        fields = ('pk', 'userName', 'stuCode', 'email', 'phoneNum',
                  'password', 'school', 'college', 'major', 'subordinateClass', 'selectionLog')

        # def create(self, validated_data):
        #     new_user = User.objects.create(
        #         userName=validated_data['userName'],
        #         stuCode=validated_data['stuCode'],
        #         email=validated_data['email'],
        #         phoneNum=validated_data['phoneNum'],
        #         password=md5(validated_data['password']),
        #         school=validated_data['school'],
        #         college=validated_data['college'],
        #         major=validated_data['major'],
        #         subordinateClass=validated_data['subordinateClass']
        #     )
        #     return new_user


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ('pk', 'name', 'offcialLink')


class CourseSerializer(serializers.ModelSerializer):
    selectionLog = serializers.PrimaryKeyRelatedField(many=True, queryset=SelectionLog.objects.all())

    class Meta:
        model = Course
        fields = ('pk', 'name', 'subordinateSchoolAndCollege', 'openTime',
                  'period', 'info', 'link', 'selectionLog')


class SelectionLogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.userName')
    selectedCourse = serializers.ReadOnlyField(source='selectedCourse.name')

    class Meta:
        model = SelectionLog
        fields = ('pk', 'user', 'selectedCourse', 'valid')


def md5(text):
    hashlib.md5(text.encode(encoding='UTF-8')).hexdigest();
