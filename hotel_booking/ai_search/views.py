from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hotels.serializers import HotelRoomSerializer

from .serializers import SearchSerializer
from .services import AISearchService


class NaturalLanguageSearchView(APIView):
     
    permission_classes = [IsAuthenticated]

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