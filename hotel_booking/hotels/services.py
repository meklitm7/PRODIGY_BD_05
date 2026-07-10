from django.core.cache import cache

from .models import HotelRoom


class HotelRoomService:
     
    CACHE_TIMEOUT = 300

    @staticmethod
    def get_all_rooms():

        cache_key = "all_rooms"

        rooms = cache.get(cache_key)

        if rooms is None:

            print("Loading rooms from MySQL...")

            rooms = HotelRoom.objects.all()

            cache.set(
                cache_key,
                rooms,
                timeout=HotelRoomService.CACHE_TIMEOUT,
            )

        else:

            print("Loading rooms from Redis...")

        return rooms

    @staticmethod
    def search_rooms(queryset, query_params):

        cache_key = (
            f"rooms:{query_params.urlencode()}"
            if query_params
            else "rooms:all"
        )

        rooms = cache.get(cache_key)

        if rooms is None:

            print("Loading search results from MySQL...")

            rooms = queryset

            cache.set(
                cache_key,
                rooms,
                timeout=HotelRoomService.CACHE_TIMEOUT,
            )

        else:

            print("Loading search results from Redis...")

        return rooms

    @staticmethod
    def get_room_by_id(room_id):

        cache_key = f"room:{room_id}"

        room = cache.get(cache_key)

        if room is None:

            print("Loading room from MySQL...")

            room = HotelRoom.objects.get(id=room_id)

            cache.set(
                cache_key,
                room,
                timeout=HotelRoomService.CACHE_TIMEOUT,
            )

        else:

            print("Loading room from Redis...")

        return room

    @staticmethod
    def clear_room_cache():

        cache.delete("all_rooms")

        cache.delete_pattern("rooms:*")

        cache.delete_pattern("room:*")

    @staticmethod
    def create_room(owner, validated_data):

        room = HotelRoom.objects.create(
            owner=owner,
            **validated_data,
        )

        HotelRoomService.clear_room_cache()

        return room

    @staticmethod
    def update_room(room, validated_data):

        for field, value in validated_data.items():

            setattr(room, field, value)

        room.save()

        HotelRoomService.clear_room_cache()

        return room

    @staticmethod
    def delete_room(room):

        HotelRoomService.clear_room_cache()

        room.delete()