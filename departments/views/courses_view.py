from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from users.models.user_model import User
from ..models import Course
from ..serializers import CourseSerializer
from users.utils.permission_management import InstructorPermission, StudentPermission

class CoursesView(APIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @permission_classes([InstructorPermission | StudentPermission])
    def get(self, request, courseId = None):
        try:
            if courseId:
                course = self.queryset.get(id=courseId)
                serializer = self.serializer_class(course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                courses = self.queryset.all()
                limit = request.data.get('limit') or 10
                offset = request.data.get('offset') or 0
                serializer = self.serializer_class(courses, many=True)
                limited_data = serializer.data[offset:offset+limit]
                return Response(limited_data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"message": "Course Does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    @permission_classes([InstructorPermission])
    def post(self, request):
        try:
            if self.serializer_class.is_valid():
                self.serializer_class.save()
                return Response(self.serializer_class.cleaned_data, status=status.HTTP_201_CREATED)
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_classes([InstructorPermission])
    def delete(self, request, courseId):
        try:
            course = self.queryset.get(id=courseId)
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({"message": "Course Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_classes([InstructorPermission])
    def patch(self, request, courseId):
        try:
            course = self.queryset.get(id=courseId)
            if self.serializer_class.is_valid() and course is not None:
                self.serializer_class.save()
                return Response(self.serializer_class.data, status=status.HTTP_200_OK)
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({"message": "Course Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class getDepartmentCourses(APIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [StudentPermission | InstructorPermission]

    def get(self, request, departmentId):
        try:
            if departmentId is not None:
                department_courses = self.queryset.filter(departmentId=departmentId)
                serializedData = self.serializer_class(department_courses, many=True)

                return Response(serializedData.data, status=status.HTTP_200_OK)
            else:
                raise Exception("Department ID is required")
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PurchaseCoursesView(APIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [StudentPermission]

    def post(self, request, courseId, userId):
        try:
            course = self.queryset.get(courseId=courseId)
            user = User.objects.get(id=userId)
            user.courses.add(course)
            return Response({"message": "Course Purchased Successfully"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"message": "Course Does not exist"}, status=status.HTTP_404_NOT_FOUND)