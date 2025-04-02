from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from ..serializers import UserSerializer


class UserView(APIView):
    def get(self, request, userId):
        try:
            if userId is not None:
                user = User.objects.get(id=userId)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentsView(APIView):
    def get(self, request):
        try:
            students = User.objects.filter(is_student=True)
            serializer = UserSerializer(students, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class InstructorsView(APIView):
    def get(self, request):
        try:
            instructors = User.objects.filter(is_instructor=True)
            serializer = UserSerializer(instructors, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)