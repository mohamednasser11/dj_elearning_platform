#TODO:: we need to create a seperate model for the instructor logic as it will be complex for the freelance part
from ..models import User, Instructor
from ..serializers import UserSerializer, InstructorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class InstructorFreelanceView(APIView):

    def post(self, request, userId):
        if userId:
            try:
                user = User.objects.get(id=userId)
                if Instructor.objects.filter(user=user).exists():
                    return Response({"error": "User is already an instructor."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    Instructor.objects.create(user=user)
                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def get(self, request):
        try:
            instructors = Instructor.objects.all()
            serializer = InstructorSerializer(instructors, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)