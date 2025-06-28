from django.urls import path
from django.views.generic.base import TemplateView
from .views import ListApple
from .views import CsrfProtectedForm
from .views import ProtectedView


app_name='gview'


urlpatterns = [
    # Wired an index or anything view into the URLconf
    path(
        '', 
        TemplateView.as_view(template_name="gview/index.html"), 
        name="gview-index"
    ),
    path('apples', ListApple.as_view(), name='apple-list'),
    path('guess', CsrfProtectedForm.as_view(), name='guess-me-protected'),
    path('protected-route', ProtectedView.as_view(), name='protected-route'),
]