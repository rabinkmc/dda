from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render
from students.models import Student, Course, Instructor, Enrollment, MetaData
from students.forms import CourseForm, StudentForm, InstructorForm, EnrollmentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

from users.permissions import is_admin, is_own_student, is_own_enrollment

User = get_user_model()


@login_required
def dashboard(request):
    total_students = Student.objects.filter(user__is_active=True).count()
    total_courses = Course.objects.filter(enrollments__isnull=False).distinct().count()
    instructors = Instructor.objects.filter(user__is_active=True).count()
    total_enrollments = Enrollment.objects.count()
    context = {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_instructors": instructors,
        "total_enrollments": total_enrollments,
    }
    return render(request, "dashboard.html", context=context)


@login_required
def student_list(request):
    students_qs = Student.objects.select_related("user")
    user = request.user
    if user.is_student:
        students_qs = students_qs.filter(user=user)

    query = request.GET.get("q")
    if query:
        students_qs = students_qs.filter(
            Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
        )

    page_number = request.GET.get("page", 1)
    page_limit = request.GET.get("limit", 10)
    paginator = Paginator(students_qs, page_limit)
    page_obj = paginator.get_page(page_number)

    students = page_obj.object_list

    return render(
        request,
        "students/student_list.html",
        {"students": students, "page_obj": page_obj},
    )


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = request.user
    if not (user.is_admin or is_own_student(user, student)):
        return HttpResponseForbidden(
            "You do not have permission to view this student's details."
        )
    return render(request, "students/student_detail.html", {"student": student})


@user_passes_test(is_admin)
def student_create(request):
    metadata_qs = MetaData.objects.all()
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
            )
            student = Student.objects.create(
                user=user,
                date_of_birth=form.cleaned_data.get("date_of_birth"),
            )
            metadata = form.cleaned_data.get("metadata", [])
            if metadata:
                student.metadata.set(metadata)
            messages.success(request, "Student has been created successfully!")
            return redirect("students:list")
    else:
        form = StudentForm()
    return render(
        request,
        "students/student_form.html",
        {"form": form, "student": None, "metadata": metadata_qs},
    )


@user_passes_test(is_admin)
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = student.user
    metadata_qs = MetaData.objects.all()
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            student.date_of_birth = form.cleaned_data.get(
                "date_of_birth", student.date_of_birth
            )
            metadata = form.cleaned_data.get("metadata", [])
            student.save()
            student.metadata.set(metadata)
            user.save()
            messages.success(
                request, "Student information has been saved successfully!"
            )
            return redirect("students:list")
        else:
            print(form.errors)

    else:
        initial_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_of_birth": student.date_of_birth,
            "email": user.email,
            "metadata": student.metadata.all(),
        }
        form = StudentForm(initial=initial_data, instance=student)
    return render(
        request,
        "students/student_form.html",
        {"form": form, "student": student, "metadata": metadata_qs},
    )


@user_passes_test(is_admin)
@require_POST
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, "Student has been deleted successfully!")
    return redirect("students:list")


@login_required
def course_list(request):
    courses = Course.objects.all()

    query = request.GET.get("q")  # search term
    if query:
        courses = courses.filter(
            Q(name__icontains=query)
            | Q(code__icontains=query)
            | Q(description__icontains=query)
        )

    page_number = request.GET.get("page", 1)
    page_limit = request.GET.get("limit", 10)
    paginator = Paginator(courses, page_limit)
    page_obj = paginator.get_page(page_number)

    courses = page_obj.object_list

    return render(
        request, "students/course_list.html", {"courses": courses, "page_obj": page_obj}
    )


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, "students/course_detail.html", {"course": course})


@user_passes_test(is_admin)
def course_create(request):
    metadata_qs = MetaData.objects.all()
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = Course.objects.create(
                name=form.cleaned_data["name"],
                code=form.cleaned_data["code"],
                description=form.cleaned_data["description"],
            )
            metadata = form.cleaned_data.get("metadata", [])
            if metadata:
                course.metadata.set(metadata)
            messages.success(request, "Course has been created successfully!")
            return redirect("students:courses-list")
    else:
        form = CourseForm()
    return render(
        request,
        "students/course_form.html",
        {"form": form, "course": None, "metadata": metadata_qs},
    )


@user_passes_test(is_admin)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    metadata_qs = MetaData.objects.all()
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course.name = form.cleaned_data["name"]
            course.code = form.cleaned_data["code"]
            course.description = form.cleaned_data["description"]
            metadata = form.cleaned_data.get("metadata", [])
            course.save()
            course.metadata.set(metadata)
            messages.success(request, "Course has been updated successfully!")
            return redirect("students:courses-list")
    else:
        initial_data = {
            "name": course.name,
            "code": course.code,
            "description": course.description,
            "metadata": course.metadata.all(),
        }
        form = CourseForm(initial=initial_data, instance=course)
    return render(
        request,
        "students/course_form.html",
        {"form": form, "course": course, "metadata": metadata_qs},
    )


@user_passes_test(is_admin)
@require_POST
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, "Course has been deleted successfully!")
    return redirect("students:courses-list")


@login_required
def instructor_list(request):
    instructors = Instructor.objects.select_related("user").prefetch_related("courses")

    query = request.GET.get("q")  # search term
    if query:
        instructors = instructors.filter(
            Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
        )

    page_number = request.GET.get("page", 1)
    page_limit = request.GET.get("limit", 10)
    paginator = Paginator(instructors, page_limit)
    page_obj = paginator.get_page(page_number)

    instructors = page_obj.object_list

    return render(
        request,
        "students/instructor_list.html",
        {
            "instructors": instructors,
            "page_obj": page_obj,
        },
    )


@login_required
def instructor_detail(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    return render(
        request, "students/instructor_detail.html", {"instructor": instructor}
    )


@user_passes_test(is_admin)
def instructor_create(request):
    courses = Course.objects.all()
    metadata_qs = MetaData.objects.all()
    if request.method == "POST":
        form = InstructorForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
            )
            instructor = Instructor.objects.create(user=user)
            courses_selected = form.cleaned_data.get("courses", [])
            metadata = form.cleaned_data.get("metadata", [])
            if courses_selected:
                instructor.courses.set(courses_selected)
            if metadata:
                instructor.metadata.set(metadata)
            messages.success(request, "Instructor has been created successfully!")
            return redirect("students:instructors-list")
    else:
        form = InstructorForm()
    return render(
        request,
        "students/instructor_form.html",
        {"form": form, "instructor": None, "courses": courses, "metadata": metadata_qs},
    )


@user_passes_test(is_admin)
def instructor_update(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    user = instructor.user
    courses = Course.objects.all()
    metadata_qs = MetaData.objects.all()
    if request.method == "POST":
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            instructor.save()
            courses_selected = form.cleaned_data.get("courses", [])
            metadata = form.cleaned_data.get("metadata", [])
            instructor.courses.set(courses_selected)
            instructor.metadata.set(metadata)
            messages.success(
                request, "Instructor information has been saved successfully!"
            )
            return redirect("students:instructors-list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "courses": instructor.courses.all(),
            "metadata": instructor.metadata.all(),
        }
        form = InstructorForm(initial=initial_data, instance=instructor)

    return render(
        request,
        "students/instructor_form.html",
        {
            "form": form,
            "instructor": instructor,
            "courses": courses,
            "metadata": metadata_qs,
        },
    )


@user_passes_test(is_admin)
@require_POST
def instructor_delete(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    instructor.delete()
    messages.success(request, "Instructor has been deleted successfully!")
    return redirect("students:instructors-list")


@login_required
def enrollment_list(request):
    if is_admin(request.user):
        enrollments = Enrollment.objects.all()
    else:
        enrollments = Enrollment.objects.filter(student__user=request.user)

    query = request.GET.get("q")
    if query:
        enrollments = enrollments.filter(
            Q(student__user__first_name__icontains=query)
            | Q(student__user__last_name__icontains=query)
            | Q(course__name__icontains=query)
            | Q(course__code__icontains=query)
        )

    page_number = request.GET.get("page", 1)
    page_limit = request.GET.get("limit", 2)
    paginator = Paginator(enrollments, page_limit)
    page_obj = paginator.get_page(page_number)

    enrollments = page_obj.object_list

    return render(
        request,
        "students/enrollment_list.html",
        {"enrollments": enrollments, "page_obj": page_obj},
    )


@login_required
def enrollment_detail(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    user = request.user
    if not (user.is_admin or is_own_enrollment(user, enrollment)):
        return HttpResponseForbidden(
            "You don't have permission to view this enrollment."
        )
    return render(
        request, "students/enrollment_detail.html", {"enrollment": enrollment}
    )


@user_passes_test(is_admin)
def enrollment_create(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    metadata_qs = MetaData.objects.all()
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = Enrollment.objects.create(
                student=form.cleaned_data["student"],
                course=form.cleaned_data["course"],
                grade=form.cleaned_data.get("grade"),
                score=form.cleaned_data.get("score"),
            )
            metadata = form.cleaned_data.get("metadata", [])
            if metadata:
                enrollment.metadata.set(metadata)
            messages.success(request, "Enrollment has been created successfully!")
            return redirect("students:enrollments-list")
    else:
        form = EnrollmentForm()
    context = {
        "form": form,
        "enrollment": None,
        "students": students,
        "courses": courses,
        "metadata": metadata_qs,
    }
    return render(request, "students/enrollment_form.html", context=context)


@user_passes_test(is_admin)
def enrollment_update(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    students = Student.objects.all()
    courses = Course.objects.all()
    metadata_qs = MetaData.objects.all()
    if request.method == "POST":
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            enrollment.student = form.cleaned_data["student"]
            enrollment.course = form.cleaned_data["course"]
            enrollment.grade = form.cleaned_data.get("grade")
            enrollment.score = form.cleaned_data.get("score")
            metadata = form.cleaned_data.get("metadata", [])
            enrollment.save()
            enrollment.metadata.set(metadata)
            messages.success(request, "Enrollment has been updated successfully!")
            return redirect("students:enrollments-list")
    else:
        initial_data = {
            "student": enrollment.student.id,
            "course": enrollment.course.id,
            "enrollment_date": getattr(enrollment, "enrollment_date", None),
            "grade": getattr(enrollment, "grade", None),
            "score": getattr(enrollment, "score", None),
            "metadata": enrollment.metadata.all(),
        }
        form = EnrollmentForm(initial=initial_data, instance=enrollment)
    return render(
        request,
        "students/enrollment_form.html",
        {
            "form": form,
            "enrollment": enrollment,
            "students": students,
            "courses": courses,
            "metadata": metadata_qs,
        },
    )


@user_passes_test(is_admin)
@require_POST
def enrollment_delete(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    enrollment.delete()
    messages.success(request, "Enrollment has been deleted successfully!")
    return redirect("students:enrollments-list")
