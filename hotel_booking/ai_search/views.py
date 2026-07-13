from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hotels.serializers import HotelRoomSerializer

from .serializers import SearchSerializer
from .services import AISearchService
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)

class NaturalLanguageSearchView(APIView):
     
    permission_classes = [IsAuthenticated]

    @extend_schema(
    summary="Natural Language Hotel Search",
    description=(
        "Search hotel rooms using natural language.\n\n"
        "Examples:\n"
        "- Luxury suite tomorrow\n"
        "- Cheap room in Addis Ababa\n"
        "- Suite for 2 guests this weekend\n"
        "- Room under 3000"
    ),
    request=SearchSerializer,
    responses=HotelRoomSerializer(many=True),
    examples=[
        OpenApiExample(
            "Search Example",
            value={
                "query": "Luxury suite tomorrow"
            },
            request_only=True,
        )
    ],
)

    def post(self, request):
         
        serializer = SearchSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        query = serializer.validated_data["query"]

        rooms = AISearchService.search(query)

        return Response(
            HotelRoomSerializer(
                rooms,
                many=True,
            ).data
        )