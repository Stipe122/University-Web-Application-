from django.http import HttpResponse

def admin_only(function):
    def wrap(*args, **kwargs):
        if args[0].user.role.name == "Administrator":
            return function(*args, **kwargs)
        else:
            return HttpResponse('<h3> You are not allowed to access this page. </h3>')
    return wrap

def professor_only(function):
    def wrap(*args, **kwargs):
        if args[0].user.role.name == "Professor":
            return function(*args, **kwargs)
        else:
            return HttpResponse('<h3> You are not allowed to access this page. </h3>')
    return wrap

def student_only(function):
    def wrap(*args, **kwargs):
        if args[0].user.role.name == "Student":
            return function(*args, **kwargs)
        else:
            return HttpResponse('<h3> You are not allowed to access this page. </h3>')
    return wrap

def admin_and_professor_only(function):
    def wrap(*args, **kwargs):
        if args[0].user.role.name == "Administrator" or args[0].user.role.name == "Professor":
            return function(*args, **kwargs)
        else:
            return HttpResponse('<h3> You are not allowed to access this page. </h3>')
    return wrap