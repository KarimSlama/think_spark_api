from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.serializers.serializer import ConversationDetailSerializer
from .models import Conversation


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_conversations(request):
    conversations = Conversation.objects.filter(participants=request.user).prefetch_related(
        'participants',
        'messages',
        'messages__sender',
        'messages__sender__profile'
    ).order_by('-created_at')
    
    serializer = ConversationDetailSerializer(
        conversations, 
        many=True,
        context={'request': request}
    )
    
    return Response({
        "success": True,
        "message": "Conversations retrieved successfully.",
        "conversations": serializer.data
    })