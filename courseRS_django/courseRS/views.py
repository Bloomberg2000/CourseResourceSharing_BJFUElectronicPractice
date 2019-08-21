from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courseRS import models
from courseRS.models import User, College, Course, SelectionLog
from courseRS.serializers import UserSerializer, CollegeSerializer, CourseSerializer, \
    SelectionLogSerializer
from django.db.models import Q
from courseRS.utils import md5, is_login, who_is_login


class AuthView(APIView):
    def get(self, request):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        request.session.flush()
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        if userName and password:
            try:
                current_user = models.User.objects.get(
                    Q(userName=userName) | Q(phoneNum=userName) | Q(email=userName) | Q(stuCode=userName))
                password = md5(password)
                if current_user.password == password:
                    request.session['ISLOGIN'] = "true"
                    request.session['USERUNIQUEID'] = current_user.pk
                    return Response({"userID": [current_user.pk]}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            except models.User.DoesNotExist:
                return Response({"detail": ["User dose not exist"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": ["Please make sure you fill in the required fields."]},
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
            return Response({"detail": ["Please Login First."]},
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
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        if who_is_login(request) != self.get_object().pk:
            return Response({"detail": ["No permission, please log in with the corresponding account"]},
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

    def post(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class CollegeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

    def put(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def put(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


class SelectionLogList(generics.ListCreateAPIView):
    queryset = SelectionLog.objects.all()
    serializer_class = SelectionLogSerializer

    def get(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        self.queryset = SelectionLog.objects.filter(user=who_is_login(request)).all()
        response = super().get(request, *args, **kwargs)
        self.queryset = SelectionLog.objects.all()
        return response

    def post(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class SelectionLogDetail(generics.RetrieveAPIView):
    queryset = SelectionLog.objects.all()
    serializer_class = SelectionLogSerializer

    def get(self, request, *args, **kwargs):
        if not is_login(request):
            return Response({"detail": ["Please Login First."]},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)
