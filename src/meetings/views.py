from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from meetings.serializers.meeting_serializer import MeetingSerializer
from .models import Idea, Meeting
import firebase_admin
from firebase_admin import credentials, messaging
import random

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_meeting(request):
    idea_id = request.data.get('idea_id')
    datetime_str = request.data.get('scheduled_datetime')

    try:
        idea = Idea.objects.get(id=idea_id)
    except Idea.DoesNotExist:
        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'Idea not found',
            'data': []
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        meeting = Meeting.objects.create(
            idea=idea,
            investor=request.user,
            scheduled_datetime=datetime_str
        )

        titles = [
            'A meeting has been scheduled for your idea',
            'Harry Up! Your idea meeting is set',
            'Your idea meeting has been scheduled',
            'The meeting for your idea has been scheduled',
            'Your upcoming meeting regarding your idea',
            'The meeting request for your idea has been made'
        ]

        selected_title = random.choice(titles)

        creative_profile = idea.user.profile
        print("Device Token:", creative_profile.device_token)

        if creative_profile.device_token:
            send_notification(
                token=creative_profile.device_token,
                title=selected_title,
                body=f'"{idea.user.username}"has been scheduled a meeting for your idea "{idea.title}"',
            )

    except Exception as e:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': f'Error creating meeting: {str(e)}',
            'data': []
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = MeetingSerializer([meeting], many=True)
    return Response({
        'status': status.HTTP_201_CREATED,
        'message': 'Meeting scheduled successfully',
        'data': serializer.data
    }, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_scheduled_meetings(request):
    user = request.user
    meetings = Meeting.objects.filter(investor=user).select_related('idea')

    serializer = MeetingSerializer(meetings, many=True)
    return Response({
        'status': status.HTTP_200_OK,
        'message': 'Meetings retrieved successfully',
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_device_token(request):
    token = request.data.get('device_token')
    if not token:
        return Response({'error': 'Token is required'}, status=400)

    profile = request.user.profile
    profile.device_token = token
    profile.save()
    print("Device Token SAVE DEV:", profile.device_token)
    return Response({'message': 'Token saved successfully'})


cred = credentials.Certificate('E:/Django Projects/think-spark-1c5d6-firebase-adminsdk-fbsvc-976e200044.json')
firebase_admin.initialize_app(cred)

def send_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)