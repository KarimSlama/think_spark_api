from rest_framework.response import Response
from rest_framework.decorators import api_view
from preferences.models import Preferences
from preferences.serializers.preferences_serializer import PreferencesSerializer

@api_view(['GET'])
def category_list(request):
    categories = Preferences.objects.filter(type='category')

    serializer = PreferencesSerializer(categories, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def filter_list(request):
    filters = Preferences.objects.filter(type='filter')

    serializer = PreferencesSerializer(filters, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def location_list(request):
    locations = Preferences.objects.filter(type='location')

    serializer = PreferencesSerializer(locations, many=True)

    return Response(serializer.data)
