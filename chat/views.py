from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat.models import ChatSession
from departments.models.courses_models.course_models import Course


class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ["id", "created_at", "updated_at"]


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, courseId):
        try:
            if courseId:
                course = Course.objects.get(courseId=courseId)
                sessions = ChatSession.objects.filter(user=request.user, course=course)
                print(list(sessions))
                serialized_sessions = []
                for session in sessions:
                    serialized_sessions.append(ChatSessionSerializer(session).data)
                return Response(
                    serialized_sessions,
                    status=status.HTTP_200_OK,
                )

        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )
