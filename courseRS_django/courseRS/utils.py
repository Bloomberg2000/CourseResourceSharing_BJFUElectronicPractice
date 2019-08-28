import hashlib

from rest_framework.pagination import PageNumberPagination


def md5(text):
    return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()


def is_login(request):
    return True if (request.session.get('ISLOGIN') == 'true') else False


def who_is_login(request):
    return request.session.get('USERUNIQUEID')

class UserType:
    STUDENT = 0
    ADMIN = 1

class StandardPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 10
    # 默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"

