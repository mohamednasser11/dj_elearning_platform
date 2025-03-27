from .departments_models import Departments
from .courses_models.courses_of_department_model import CoursesOfDepartment
from .courses_models.course_models import Course
from .courses_models.course_lesson_models import CoursesLesson
from .courses_models.user_courses_purchase_model import UserCoursePurchase


__all__ = ['Departments' , 'Course', 'CoursesOfDepartment', 'CoursesLesson', 'UserCoursePurchase']