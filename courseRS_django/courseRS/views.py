import json

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courseRS import models
from courseRS.filters import CollegeFilter, CourseFilter
from courseRS.models import User, College, Course, SelectionLog
from courseRS.mooc_helper import crawl_mooc
from courseRS.serializers import UserSerializer, CollegeSerializer, CourseSerializer, \
    SelectionLogSerializer
from django.db.models import Q
from courseRS.utils import md5, is_login, who_is_login, StandardPagination


class AuthView(APIView):
    def get(self, request):
        request.session.flush()
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        if userName and password:
            try:
                current_user = models.User.objects.get(Q(userName=userName) | Q(phoneNum=userName) | Q(email=userName))
                password = md5(password)
                if current_user.password == password:
                    request.session['ISLOGIN'] = "true"
                    request.session['USERUNIQUEID'] = current_user.pk
                    return Response({"userID": [current_user.pk], "userType": [current_user.type]},
                                    status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"detail": ["密码错误"]}, status=status.HTTP_400_BAD_REQUEST)
            except models.User.DoesNotExist:
                return Response({"detail": ["用户不存在"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": ["请确认必填字段已填写"]},
                            status=status.HTTP_400_BAD_REQUEST)


# 创建用户
class UserList(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 查看/编辑/修改用户
class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 获取用户信息
    def get(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = dict(serializer.data)
        del data['password']  # 移除密码信息
        # 非本人查看删除用户信息
        if who_is_login(request) != instance.pk:
            del data['phoneNum']
            del data['email']
        return Response(data)

    # 禁止通过PUT修改用户
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Method \"PUT\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # 编辑用户信息
    def patch(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        if who_is_login(request) != self.get_object().pk:
            return Response({"detail": ["权限不足，请使用对应账号登录"]},
                            status=status.HTTP_403_FORBIDDEN)
        # 如果要修改密码进行对应判断
        if request.POST.__contains__('password'):
            # 是否传递原密码
            if request.POST.__contains__('oldPassword'):
                user = self.get_object()
                # 原密码是否正确
                if md5(request.POST['oldPassword']) == user.password:
                    return super().patch(request, *args, **kwargs)
                else:
                    return Response({"oldPassword": ["Wrong oldPassword"]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"oldPassword": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        return super().patch(request, *args, **kwargs)


class CollegeList(generics.ListCreateAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    pagination_class = StandardPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = CollegeFilter

    def post(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class CollegeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

    def put(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = CourseFilter

    def post(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def put(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


class SelectionLogList(generics.ListCreateAPIView):
    queryset = SelectionLog.objects.all().filter(valid=1)
    serializer_class = SelectionLogSerializer
    pagination_class = StandardPagination

    def get(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        self.queryset = SelectionLog.objects.filter(user=who_is_login(request)).filter(valid=True).order_by('-time').all()
        response = super().get(request, *args, **kwargs)
        self.queryset = SelectionLog.objects.all()
        return response

    def post(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class SelectionLogDetail(generics.RetrieveUpdateAPIView):
    queryset = SelectionLog.objects.filter(valid=True).all()
    serializer_class = SelectionLogSerializer

    def get(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)

    # 禁止通过PUT修改
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Method \"PUT\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # 编辑用户信息
    def patch(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["请先登录"]},
                            status=status.HTTP_401_UNAUTHORIZED)
        if who_is_login(request) != self.get_object().user_id:
            return Response({"detail": ["权限不足，请使用对应账号登录"]},
                            status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)


def updateCourse(request):
    crawl_mooc()
    return HttpResponse(json.dumps("OK", ensure_ascii=False), content_type="application/json,charset=utf-8")
