import hashlib


def md5(text):
    return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()


def is_login(request):
    return True if (request.session.get('ISLOGIN') == 'true') else False


def who_is_login(request):
    return request.session.get('USERUNIQUEID')


class UserType:
    STUDENT = 0
    ADMIN = 1
