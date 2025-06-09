from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Departments, Course, CoursesLesson
from ..serializers.lessons_serialzer import LessonSerializer
from users.utils.permission_management import InstructorPermission, StudentPermission


class LessonsView(APIView):
    permission_classes = [IsAuthenticated, InstructorPermission | StudentPermission]

    def get(self, request, courseId, lessonId=None):
        try:
            if lessonId and courseId:
                course = Course.objects.get(id=courseId)
                lesson = CoursesLesson.objects.filter(course=course).get(id=lessonId)
                serializer = LessonSerializer(lesson)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                course = Course.objects.get(id=courseId)
                lessons = CoursesLesson.objects.filter(course=course)
                serializer = LessonSerializer(lessons, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Departments.DoesNotExist:
            return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except CoursesLesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)
 
    def post(self, request, courseId):
        try:
            course = Course.objects.get(courseId=courseId)
            request.data['courseId'] = course.courseId
            serializer = LessonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, courseId):
        try:
            if courseId is not None and 'lessonId' in request.data:
                course = Course.objects.get(courseId=courseId)
                lesson = CoursesLesson.objects.filter(course=course).get(id=request.data['lessonId'])
                serializer = LessonSerializer(lesson, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'lessonId is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except CoursesLesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, courseId, lessonId):
        try:
            course = Course.objects.get(courseId=courseId)
            lesson = CoursesLesson.objects.get(course=course, lessonId=lessonId)
            if lesson:
                lesson.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except CoursesLesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)