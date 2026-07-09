from rest_framework.routers import DefaultRouter

from .views import HotelRoomViewSet

router = DefaultRouter()

router.register(
    "rooms",
    HotelRoomViewSet,
    basename="rooms",
)

urlpatterns = router.urls