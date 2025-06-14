import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from users.models.user_model import User
from ..models import Course
from ..serializers import CourseSerializer
from users.utils.permission_management import InstructorPermission, StudentPermission
from users.models.instructor_model import InstructorModel

class CoursesView(APIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @permission_classes([InstructorPermission | StudentPermission])
    def get(self, request, courseId = None):
        try:
            if courseId:
                course = self.queryset.get(courseId = courseId)
                serializer = self.serializer_class(course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                courses = self.queryset.all()
                limit = int(request.GET.get('limit', 10))
                offset = int(request.GET.get('offset', 10))
                serializer = self.serializer_class(courses, many=True)
                limited_data = serializer.data[offset:offset+limit]
                return Response(limited_data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"message": "Course Does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            print(f'user data: {request.user}')
            # Get the instructor model associated with the authenticated user
            instructor = InstructorModel.objects.get(user=request.user)

            # Inject the instructor ID into the data before serialization
            data["instructorId"] = instructor.user_id

            serialized_course = self.serializer_class(data=data)
            if serialized_course.is_valid():
                serialized_course.save()
                return Response({"message": "created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serialized_course.errors, status=status.HTTP_400_BAD_REQUEST)

        except InstructorModel.DoesNotExist:
            return Response({"message": "User is not registered as an instructor"}, status=status.HTTP_403_FORBIDDEN)
        
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
            data=json.loads(request.body)
            course = self.queryset.get(courseId=courseId)
            instructor = InstructorModel.objects.get(user=request.user)

            # Inject the instructor ID into the data before serialization
            data["instructorId"] = instructor.user_id
            serialized_new_course = self.serializer_class(data=data)
            if serialized_new_course.is_valid() and course is not None:
                serialized_new_course.save()
                return Response(serialized_new_course.data, status=status.HTTP_200_OK)
            return Response(serialized_new_course.errors, status=status.HTTP_400_BAD_REQUEST)
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
