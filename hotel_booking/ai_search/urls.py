from django.urls import path

from .views import NaturalLanguageSearchView

urlpatterns = [
    path(
        "search/",
        NaturalLanguageSearchView.as_view(),
        name="ai-search",
    ),
]