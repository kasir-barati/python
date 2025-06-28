from typing import NoReturn
from ..models import Movie


class MovieRepository:
    def find_by_id(self, id: int,) -> Movie:
        movie = Movie.objects.get(pk=id)
        return movie

    # TODO: Annotate return type if possible
    def find_all(self,):
        return Movie.objects.all()

    """
    TODO: find a way to annotate "movie" automatically
    FIXME: Here also we have a bad time. I do not know how to decouple
    Service layer from the serializer layer and at the same time be
    strongly typed. Based on onion architecture I should not couple
    my service layer to serializer. BTW one way is to use TypedDict
    which is too much maybe.

    FIXME: No way to return updated record?
    """
    def update_by_id(self, id: int, movie,) -> None:
        """
        The same goes ont here. I used get over filter for simplicity
        """
        updated_movies_count = Movie.objects.filter(pk=id).update(
            name=movie['name'],
            active=movie['active'],
            description=movie['description'],
        )
        
        if updated_movies_count == 0:
            raise Movie.DoesNotExist()
        
        """
        Based on my observation from The Pragmatic Programmer I check something that its
        probability is less than 0. Assertive programming section.
        """
        assert updated_movies_count == 1, "Too many - more than one - movie has been updated"
        
        return

    def delete_by_id(self, id: int,) -> None|NoReturn:
        """
        README: Movie.objects.filter(pk=id).delete() won't throw error if record
        does not exists. But I have two options here:
            1. Stick to this solution:
                if affected_movies_count > 1:
                    raise Exception("Too many item affected")
                if affected_movies_count == 0:
                    raise Movie.DoesNotExist()
            2. Use the ORM, Movie.objects.get(pk=id).delete() this snippet does both
            off those validations. But I guess I am performing two queries against
            db, one to fetch record and another to delete record. It now completely
            is based on situation; 
                1. If I/O matters more that codebase I will go with former option
                2. If I/O do not matter I prefer the last one since less code means
                less bug.
        """
        Movie.objects.get(pk=id).delete()        

