from django.http.request import HttpRequest
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render


def index(req: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "Hello, world. You're at the polls index."
    )
    
class GameView(View):
    # This "get" specify the HTTP verb
    def get(self, req: HttpRequest, guess: int) -> HttpResponse:
        data = { "user_guess": guess }
        return render(req, 'polls/user_guess.html', data)