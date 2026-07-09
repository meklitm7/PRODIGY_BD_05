from .models import HotelRoom


class HotelRoomService:
    """
    Business logic for hotel rooms.
    """

    @staticmethod
    def get_all_rooms():

        return HotelRoom.objects.all()

    @staticmethod
    def get_room_by_id(room_id):

        return HotelRoom.objects.get(id=room_id)

    @staticmethod
    def create_room(owner, validated_data):

        return HotelRoom.objects.create(
            owner=owner,
            **validated_data,
        )