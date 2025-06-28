import os
from typing import NoReturn
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from django.core.files import File
from django.utils import timezone
from django.core.files import File
from .tasks import celery_generate_mpd
from ..utils.save_uploaded_file import save_uploaded_file
from .repositories import MovieRepository
from ..models import Movie
from ..utils.save_uploaded_file import random_filename
from anime_die_heart.settings import MEDIA_ROOT, MEDIA_URL


class MovieService:
    def __init__(self) -> None:
        self.__movie_repository = MovieRepository()
    
    def get_object(self, id: int,):
        try:
            return self.__movie_repository.find_by_id(id)
        except Movie.DoesNotExist:
            raise NotFound(detail='Movie does not exists')
    
    def get_all(self,):
        return self.__movie_repository.find_all()
    
    def upload_file(self, file: File):
        filename = random_filename(file.name)
        original_video_abs_path = os.path.join(
            MEDIA_ROOT, 
            filename,
        )
        save_uploaded_file(
            absolute_path=original_video_abs_path,
            file=file,
        )
        mpd_filename = random_filename(
            file.name,
        )
        pure_filename, extension = os.path.splitext(mpd_filename)
        mpd_file_absolute_path = os.path.join(
            MEDIA_ROOT, 
            pure_filename + '.mpd',
        )
        """
        FIXME: make mpd_file_absolute_path null for this record
        1. Retry X time
        2. If it exceeded X then push it into a new unprocessed_error_queue or email someone or log it
        3. Find this record in database and set mpd_file_absolute_path equal to null
            3.1. Push it ino another queue named error_queue for more process
            3.2. Notify someone to check what is going and do something for those un-resized movies
        """
        celery_generate_mpd.apply_async([
            original_video_abs_path,
            mpd_file_absolute_path,
        ])

        # Timezone is really a hard thing to deal. So I decided to keep it in zero timezone
        # Read USE_TZ and generate time based on this setting
        now = timezone.now()
        created_movie = Movie.objects.create(
            name=file.name,
            description=f"File uploaded at {now}",
            active=True,
            file_name=original_video_abs_path,
            mpd_file_absolute_path=mpd_file_absolute_path
        )

        return created_movie
    
    """
    Based on onion architecture layer I decided to annotate
    movie with Movie model instead of serializer. Inner layers
    should not dependent to outer layers. Repository/Service layer
    should not be dependent to the View/Controller layer

    TODO: find a way to annotate "movie" automatically
    FIXME: Return updated record
    """
    def update_movie(self, id: int, movie,) -> None|NoReturn:
        try:
            self.__movie_repository.update_by_id(id, movie)
            return
        except Movie.DoesNotExist:
            raise NotFound(detail="Movie not found")
    
    def delete_movie(self, id: int) -> int|NoReturn:
        try:
            self.__movie_repository.delete_by_id(id)
            # TODO: delete the movie from file system too

            return id

        except Movie.DoesNotExist:
            raise NotFound(detail="Movie not found")

    def stream_video(
            self, 
            req: Request,
            mpd_file_abs_path: str) -> str:
        filename = os.path.basename(mpd_file_abs_path)
        return req.get_host() + MEDIA_URL + filename

