from django.urls import path
from .views import movie_list
from .views import movie_details

urlpatterns = [
    path('', movie_list),
    path('<int:id>', movie_details)
]

"""
Wrong usage:

- anime_die_heart/urls.py:
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('watch_list_app.urls')),
]

- watch_list_app/urls.py
from django.urls import path
from .views import movie_list

urlpatterns = [
    path('/', movie_list)
]
"""