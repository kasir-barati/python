# [Class-based Views](https://www.django-rest-framework.org/api-guide/views/)

- `APIView` which subclasses `View`
  - But they are not the same:
    - DRF `Request` instances, not Django's HttpRequest instances.
    - DRF `Response`, instead of Django's HttpResponse.
    - Any `APIException` exceptions will be caught and mediated into appropriate responses.
    - Authentication, appropriate permission checking, and/or throttle checks will be run before dispatching the request to the handler method.

# [Request object in DRF](https://www.django-rest-framework.org/api-guide/requests)

- `Request` extends the standard `HttpRequest`
  - All `HttpRequest`'s attributes and methods are available.
- Support request parsing and request authentication.
  - Treat requests with JSON data
- ## `req.data`
  - Returns the parsed content of the request body.
  - Similar to the standard `req.POST` and `req.FILES` attributes except that:
    - File and non-file inputs parsed in it
    - Pars HTTP methods bodies. Not only POST verb.
    - Pars form data and JSON data
  - If client sends malformed content, then accessing `req.data` may raise a `ParseError`.
  - By default REST framework's `APIView` class catch the error and return a 400 Bad Request response.
  - If client sends a request with a content-type that cannot be parsed then a `UnsupportedMediaType` exception will be raised
  - which by default will be caught and return a 415 Unsupported Media Type response.
- ## `req.query_params`
  - `req.query_params` is a more correctly named synonym for `req.GET`. :smile:
  - Please use this over the venerable `req.GET`. Every HTTP verb can have query string/params
- # Authentication
  - Authentication per-request.
  - Facilitate:
    - Different authentication policies for different parts of your API.
    - Multiple authentication policies.
    - User data and token information + incoming request.
  - ## `req.user`
    - an instance of `django.contrib.auth.models.User`
    - Behavior depends on the authentication policy being used.
    - `unauthenticated` request, default value of `req.user` is `django.contrib.auth.models.AnonymousUser`
  - ## `req.auth`
    - `unauthenticated` => `None`
- ## `req.meta`
  - A dictionary containing all available HTTP headers.
  - Available headers depend on the client and server. e.x.:
    - `CONTENT_LENGTH`
    - `CONTENT_TYPE`
    - `HTTP_ACCEPT`
    - `HTTP_HOST`
    - `HTTP_USER_AGENT`
    - `QUERY_STRING`
    - `REQUEST_METHOD`
    - `SERVER_NAME`
    - `SERVER_PORT`
- ## `req.method`
  - Uppercased string representation of HTTP method.
- ## `rea.stream`
  - A stream representing the content of the request body.
  - usually we do not bother ourselves and rely on DRF for parsing requests

# [Serializer](https://www.django-rest-framework.org/api-guide/serializers/)

- Convert complex data type - `querysets` and model instances - to native Python datatypes that can then be easily rendered into `JSON`.
- Deserialize parsed converted data back into complex types, after first validating the incoming data.
- ## `serializers.Serializers`
  - ### Validation
    - **Deserialize data, call `is_valid()` before attempting to do anything.**
    - If validation errors occurred, the `serializer_instance_name.errors` property will contain a dictionary representing the resulting error messages:
      ```py
      serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
      serializer.is_valid() # False
      print(serializer.errors)
      # {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}
      ```
    - `non_field_errors` list any general validation errors.
      - The `non_field_errors` key may be customized using the `NON_FIELD_ERRORS_KEY` REST framework setting.
    - Raise validation error automatically by `serializer.is_valid(raise_exception=True)`
    - #### Validate sent data against each other:
      ```py
      from rest_framework import serializers
      class PassengerSerializer(serializers.Serializer):
          passport_number: str = serializers.CharField(max_length=100)
          passport_issued_at = serializers.DateTimeField()
          passport_expire_at = serializers.DateTimeField()
          def validate(self, data):
              """
              Check that passport_issued_at is before passport_expire_at.
              """
              if data['passport_issued_at'] > data['passport_expire_at']:
                  raise serializers.ValidationError(
                      "Passport expire at must occur after passport issued at"
                  )
              return data
      ```
      - TBH I am a little shocked and I think there should be better ways to do this task
      - Besides I do not understand what is the difference between the above validator and this one:
        ```py
        class EventSerializer(serializers.Serializer):
            name: str = serializers.CharField()
            room_number: int = serializers.IntegerField(choices=[101, 102, 103, 201])
            date = serializers.DateField()
            class Meta:
                # Each room only has one event per day.
                validators = [
                    UniqueTogetherValidator(
                        queryset=Event.objects.all(),
                        fields=['room_number', 'date']
                    )
                ]
        ```
        **As far as I understand - probably it is wrong - it seems that this one validates in another level**
    - #### Custom validators for a field
      ```py
      def multiple_of_ten(value) -> None:
          if value % 10 != 0:
              raise serializers.ValidationError('Not a multiple of ten')
      class GameRecord(serializers.Serializer):
          score: int = IntegerField(validators=[multiple_of_ten])
      ```
    - #### Partial updates
      - By default, serializers must be passed values for **all required** fields or they will raise validation errors.
      - Use partial argument in order to allow partial updates.
        ```py
        serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)
        ```
    - #### Validate nested objects
      - The `Serializer` is a type of Field
      - Use it to represent relationships where one object type is nested inside another.
        ```py
        class PassengerSerializer(serializers.Serializer):
            name: str = serializers.CharField(max_length=200)
            age = serializers.DateTimeField()
        class TicketSerializer(serializers.Serializer):
            ticket_number: str = serializers.CharField(max_length=100)
            passengers: list[PassengerSerializer] = PassengerSerializer(many=True,)
            # Just in cases that we do not need to force client provide
            # us this nested object we can mark it as optional.
            # passengers = PassengerSerializer(required=False, many=True,)
        ```
        This is exactly how we act in NestJS :hooray:
  - ## `serializer.instance`
    - The passed object/queryset to the serializer
    - `None` if nothing was passed
  - ## `serializer.initial_data`
    - Unmodified data which was passed to the serializer
    - No if we do not pass `data` while instantiation - `CommentSerializer(data=something)` - this property won't exists
  - ## `serializer.validated_data`
    - Contains validated data
- ## `serializers.ModelSerializer`
  - ## Why `serializers.ModelSerializer` over `serializers.Serializer`
    - Serializer is replicating a lot of information that's also contained in the model.
    - Keep our code a bit more concise.
    - What `ModelSerializer` does:
      - An automatically determined set of fields.
      - Simple default implementations for the create() and update() methods.
  - Like a [`serializers.Serializers`](#serializersserializers) but:
    - Generate a set of fields, based on the model automatically.
    - Includes a simple default implementations of `.create()` and `.update()`.
    - Generate validators for the serializer automatically
  - By default map all the model fields to serializer fields.
  - FKs will be mapped to `PrimaryKeyRelatedField`.
  - Specify which fields to include via `fields` or `exclude` options.
    - :warning:**It is mandatory to provide one of the attributes `fields` or `exclude`.**:warning:
      ```py
      class AccountSerializer(serializers.ModelSerializer):
          class Meta:
              model = Account
              fields = ['id', 'account_name', 'users', 'created']
      ```
    - **Proclaimed by official Doc: Explicitly set all fields that should be serialized using the `fields` attribute.**
    - Less chance to unintentionally exposing data.
    - `__all__` is a specific value which means all fields.
      - TBH IDK what's the point of this option:
      - e.x. `fields = '__all__'`
  - ## **Nested serialization**
    - Uses primary keys for relationships
    - `depth` option should be set to an integer value that indicates the depth of relationships that should be traversed before reverting to a flat representation.
    - :warning:**IDK still how this work exactly. I need to test it.**:warning:
  - By redefining a field you override it
    ```py
    class AccountSerializer(serializers.ModelSerializer):
        url = serializers.CharField(source='get_absolute_url', read_only=True)
        groups = serializers.PrimaryKeyRelatedField(many=True)
        class Meta:
            model = Account
            fields = ['url', 'groups']
    ```
  - Specifying read only fields
    ```py
    class AccountSerializer(serializers.ModelSerializer):
        class Meta:
            model = Account
            fields = ['id', 'account_name', 'users', 'created']
            read_only_fields = ['account_name']
    ```

# [Exceptions](https://www.django-rest-framework.org/api-guide/exceptions/)

- Handled exceptions are:
  - `APIException`
  - `NotFound`
  - `PermissionDenied`
  - But what does it mean by handled exceptions?
    - Appropriate status code and content-type in response
