from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ideas.models import Idea
from ideas.serializers.idea_serializer import IdeaSerializer


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def idea_list_upload(request):
    if request.method == 'POST':
        serializer = IdeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'GET':
        ideas = Idea.objects.all().order_by('-created_at')
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data, status=200)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def idea_details(request, id):
    idea_details = Idea.objects.get(id=id) 
    serializer = IdeaSerializer(idea_details).data
    return Response({'data':serializer}, status=200)