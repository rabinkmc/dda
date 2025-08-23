def request_context(request):
    user = request.user
    return {
        "is_admin": getattr(user, "is_admin", False),
        "is_student": getattr(user, "is_student", False),
        "is_instructor": getattr(user, "is_instructor", False),
    }
