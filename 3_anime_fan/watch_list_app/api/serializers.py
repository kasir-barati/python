from wsgiref.util import request_uri
from rest_framework import serializers
from rest_framework.serializers import FileField
from ..models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """
    FIXME: There is a bad bug in DRF. I will fix this issue later
    https://github.com/encode/django-rest-framework/issues/1830#issuecomment-1175047486
    """
    class Meta:
        model = Movie
        read_only_fields = ('id',)
        fields = [
            'id', 
            'name', 
            'description', 
            'active', 
        ]

class UploadMovieSerializer(serializers.Serializer):
    file: FileField = serializers.FileField(
        allow_empty_file=False,
        max_length=None,
        required=True
    )

