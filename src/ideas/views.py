from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ideas.models import Idea
from ideas.serializers.idea_serializer import IdeaSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def idea_list_upload(request):
    
    if request.method == 'POST':
        serializer = IdeaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'GET':
        ideas = Idea.objects.all().order_by('-created_at')
        serializer = IdeaSerializer(ideas, many=True, context={'request': request})
        return Response(serializer.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def idea_details(request, id):
    idea_details = get_object_or_404(Idea, id=id)
    serializer = IdeaSerializer(idea_details, context={'request': request})
    return Response({'data': serializer.data}, status=200)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_idea(request, id):
    try:
        idea = Idea.objects.get(id=id)
    except Idea.DoesNotExist:
        return Response({'error': 'Idea not found'}, status=404)
    
    context = {'request': request}
    
    serializer = IdeaSerializer(idea, data=request.data, partial=True, context=context)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=404)

@api_view(['GET'])
def search_ideas(request):
    query = request.GET.get('q', '')
    if query:
        ideas = Idea.objects.filter(title__icontains=query)
    else:
        ideas = Idea.objects.all()

    serializer = IdeaSerializer(ideas, many=True, context={'request': request})
    return Response(serializer.data)