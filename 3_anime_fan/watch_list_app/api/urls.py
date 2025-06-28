from django.urls import path
from .views import UploadMovie
from .views import GetUpdateDeleteWatchList
from .views import WatchList
from .views import StreamMovie


urlpatterns = [
    path('', WatchList.as_view(), name='movies-list'),
    path(
        '<int:id>', 
        GetUpdateDeleteWatchList.as_view(), 
        name='get-update-delete-movies-list'
    ),
    path(
        'upload', 
        UploadMovie.as_view(), 
        name="upload-video"
    ),
    path(
        '<int:id>/stream',
        StreamMovie.as_view(),
        name="stream-video"
    )
]

