from django.urls import path
from .views import index
from .views import GameView


app_name='polls'


urlpatterns = [
    # Wired an index or anything view into the URLconf
    path('', index, name='index'),
    path('game/<int:guess>', GameView.as_view())
]