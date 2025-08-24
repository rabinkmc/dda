def is_admin(user):
    return user.is_authenticated and user.is_admin


def is_own_student(user, student):
    return user.is_authenticated and (user.is_student and user.student == student)


def is_own_enrollment(user, enrollment):
    return user.is_authenticated and (
        user.is_student and user.student == enrollment.student
    )
