from django.http import JsonResponse
from django.http.request import HttpRequest
from .models import Movie

# Create your views here.
def movie_list(req: HttpRequest) -> JsonResponse:
    # This will returns a QuerySet
    # <QuerySet [<Movie: Get the right job in Germany>, <Movie: Do the coding challenge>]>
    movies = Movie.objects.all()
    # Now I wanna convert the model object into dictionary
    # <QuerySet [{'id': 1, 'name': 'Get the right job in Germany', 'description': 'You can do it', 'active': True}, {'id': 2, 'name': 'Do the coding challenge', 'description': 'I am sure I can', 'active': True}]>
    movies = movies.values()
    # Next step is to get rid of that QuerySet via list
    # [{'id': 1, 'name': 'Get the right job in Germany', 'description': 'You can do it', 'active': True}, {'id': 2, 'name': 'Do the coding challenge', 'description': 'I am sure I can', 'active': True}]
    movies = list(movies)
    # Now we create response schema. But we still has to get rid of True
    # {'movies': [{'id': 1, 'name': 'Get the right job in Germany', 'description': 'You can do it', 'active': True}, {'id': 2, 'name': 'Do the coding challenge', 'description': 'I am sure I can', 'active': True}]}
    response = {"movies": movies}
    # At last we wanna get rid of those python specific and return a valid JSON response.
    # <JsonResponse status_code=200, "application/json">
    response = JsonResponse(response)
    return response


"""
Interesting enough
I do not need to convert id. I just need to tell django its type in the urls file.
I really fall in love with Django
"""
def movie_details(req: HttpRequest, id: int) -> JsonResponse:
    movie = Movie.objects.get(pk=id)
    # This print will prints "Get the right job in Germany" because of __str__
    print(movie)
    """
    Wrong usage:
    movie = vars(movie)
    """
    # Or I could define a custom method in the class named serialize response
    movie = {
        "name": movie.name,
        "description": movie.description,
        "active": movie.active
    }
    response = JsonResponse(movie)
    return response