from rest_framework.views import APIView

from users.models.user_model import User
from ..models import Course
from ..serializers import CourseSerializer
from rest_framework.response import Response
from ..forms import CoursePayloadValidation

class CoursesView(APIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, courseId = None):
        try:
            if courseId:
                course = self.queryset.get(id=courseId)
                serializer = self.serializer_class(course)
                return Response(serializer.data, status=200)
            else:
                courses = self.queryset.all()
                limit = request.data.get('limit') or 10
                offset = request.data.get('offset') or 0
                serializer = self.serializer_class(courses, many=True)
                limited_data = serializer.data[offset:offset+limit]
                return Response(limited_data)
        except Course.DoesNotExist:
            return Response({"message": "Course Does not exist"},status=404)
        
    def post(self, request): 
        try:
            form = CoursePayloadValidation(request.data)
            if form.is_valid():
                form.save()
                return Response(form.cleaned_data, status=201)
            return Response(form.errors, status=400)
        except Exception as e:
            return Response({"message": str(e)}, status=500)
    
    def delete(self, request, courseId):
        try:
            course = self.queryset.get(id=courseId)
            course.delete()
            return Response(status=204)
        except Course.DoesNotExist:
            return Response({"message": "Course Does not exist"}, status=404)
        except Exception as e:
            return Response({"message": str(e)}, status=500)

    def patch(self, request, courseId):
        try:
            course = self.queryset.get(id=courseId)
            form = CoursePayloadValidation(request.data, instance=course)
            if form.is_valid():
                form.save()
                return Response(form.cleaned_data, status=200)
            return Response(form.errors, status=400)
        except Course.DoesNotExist:
            return Response({"message": "Course Does not exist"}, status=404)
        except Exception as e:
            return Response({"message": str(e)}, status=500)
        
class PurchaseCoursesView(APIView):
    def post(self, request, courseId, userId):
        try:
            course = Course.objects.get(id=courseId)
            user = User.objects.get(id=userId)
            user.courses.add(course)
            return Response({"message": "Course Purchased Successfully"}, status=200)
        except Course.DoesNotExist:
            return Response({"message": "Course Does not exist"}, status=404)