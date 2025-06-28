# Where you can find the course?

- https://www.dj4e.com/

# What motivates me to learn it?

- TBH I am - Right now, 2022-07-02 - looking for a good opportunity in Germany. And so I am a Node.js developer. So I decided to learn what seems to be in demand
- But now I am really inspired and fascinated about python and I can say I swept of my feet :joy:

# What is going on here?

- I captured the my learning process in this repo and TBH I think I will go even further and I will create a powerful repo on top of this beautiful free course which is really doable almost I think for everyone as it is named
- I did some changes as I like so please do not expect this be the same way as it is done in the course
- When we just say `pip` or `python` it means that we wanna use python version 3
- **DRF stands for Django REST Framework**

# CLI

- `pip install -r requirements.txt` to install dependencies
- `django-admin` is a command-line utility for administrative tasks.
- A bunch of command related to `manage.py`Frw
  - Interact with this Django project
  - Automatically created.
  - `python manage.py <command> [options]`
    - Available commands:
      - **auth**
        - changepassword
        - `createsuperuser`
          - Create superusers
          - `python manage.py createsuperuser --username=Kasir --email=kasir.barati@gmail.com`
      - **contenttypes**
        - remove_stale_contenttypes
      - **django**
        - `check`: Inspect the entire Django project for common problems.
        - compilemessages
        - createcachetable
        - dbshell
        - diffsettings
        - dumpdata
        - flush
        - inspectdb
        - loaddata
        - makemessages
        - `makemigrations`:
          - Creates new migrations based on the changes detected to your models.
          - Watch our current `models.py` and see if there is any change. If there was it will create a new migration
          - **You can remove the generated migration files. Just remember that do not remove applied migration. Since Django keep track of applied migrations on the database as we have the same behavior in Prisma. But in dev env you can remove the migration file and database too.**
        - `migrate`:
          - To apply created migrations to database
        - sendtestemail
        - `shell`
          - `python manage.py shell`
          - Auto bind your projects' packages into a interactive Python
        - showmigrations
        - sqlflush
        - sqlmigrate
        - sqlsequencereset
        - squashmigrations
        - `startapp`
          - `python manage.py startapp polls`
          - A utility that automatically generates the basic directory structure of an app
          - Projects vs. apps:
            - App is a web application that does something.
            - A project is a collection of configuration and apps for a particular website.
        - `startproject` to create a new project
          - `django-admin startproject go_back_start_again`
          - Avoid naming projects after built-in Python or Django components.
          - What `startproject` created:
            - `manage.py`
            - `go_back_start_again/`:
              - root directory
            - `go_back_start_again/__init__.py`
              - Tells python to consider this directory as a Python package.
            - `go_back_start_again/settings.py`
              - Configuration for this Django project.
            - `go_back_start_again/urls.py`
              - URL declarations for this Django project
            - `go_back_start_again/asgi.py`
              - An entry-point for ASGI-compatible web servers to serve your project.
            - `go_back_start_again/wsgi.py`
              - An entry-point for WSGI-compatible web servers to serve your project.
        - test
        - testserver
      - **rest_framework**
        - generateschema
      - **sessions**
        - clearsessions
      - **staticfiles**
        - collectstatic
        - findstatic
        - `runserver`:
          - To start your app
          - Reload server automatically after you change something in codebase
            - Some actions do not cause restarting server, You have to stop and start it manually
              - One of them is adding new file
          - **Do not** use this server in anything resembling a production environment.
          - This command is tends to be only for dev env
          - Starts development server on the port 8000.
            - `python manage.py runserver 8080`
          - Starts the development server on the **internal network**
            - `python manage.py runserver 0:8000`
              - `0` is shorthand for `0.0.0.0`
    - Available options:
      - `--verbosity` To log more in terminal
      - `--deploy` to do some extra check in deploy mode
      - ``

# Steps I take in a glance

1. `mkdir d4e`
   - Put your code in some directory outside of the document root, such as `/home/mycode`.
2. `cd d3e`
3. `virtualenv venv`
4. `source venv/bin/activate`
5. `pip install django`
6. `django-admin startproject go_back_start_again`
7. `python manage.py startapp polls`

# MVC in Django

- `urls.py` are kinda our controllers
- `views.py` are view and controller
- `models.py` are models

# [`settings.py`](https://docs.djangoproject.com/en/4.0/ref/settings)

- `ALLOWED_HOSTS` tells Django to make our app available for which host/domain name. It is basically an array of strings
- Static files:
  - `STATIC_ROOT`
    - The absolute path to the directory where collectstatic will collect static files for deployment.
  - `STATIC_URL`
    - Example: "static/" or "http://static.example.com/"
  - `STATICFILES_DIRS`
    - Define additional locations for the `staticfiles`
  - `STATICFILES_STORAGE`
    - [Serving static files from a cloud service or CDN](https://docs.djangoproject.com/en/4.0/howto/static-files/deployment/#staticfiles-from-cdn).
- Logs
  - `MESSAGE_LEVEL`
    ```py
    from django.contrib.messages import constants as message_constants
    MESSAGE_LEVEL = message_constants.DEBUG
    ```
  - `MESSAGE_STORAGE`
    - `'django.contrib.messages.storage.fallback.FallbackStorage'`
    - `'django.contrib.messages.storage.session.SessionStorage'`
    - `'django.contrib.messages.storage.cookie.CookieStorage'`
- `DATA_UPLOAD_MAX_MEMORY_SIZE`
  - maximum size in bytes that a request body may be before a SuspiciousOperation (RequestDataTooBig) is raised.
  - Exclude any file upload data
  - Set to `None` to disable this check
- File upload:
  - `FILE_UPLOAD_HANDLERS`
  - `FILE_UPLOAD_MAX_MEMORY_SIZE` maximum size in bytes.
  - `FILE_UPLOAD_DIRECTORY_PERMISSIONS` numeric mode to apply to directories created in the process of uploading files.
  - `FILE_UPLOAD_PERMISSIONS` numeric mode. chmod. default `0o644`, `0o` prefix is very important
  - `FILE_UPLOAD_TEMP_DIR` directory to store data to (typically files larger than FILE_UPLOAD_MAX_MEMORY_SIZE)
- Email:
  - `EMAIL_BACKEND`:
    - `'django.core.mail.backends.console.EmailBackend'`
      - Instead of sending out real emails the console backend just writes the emails that would be sent to the standard output.
      - Just in dev mode to test that email generates successfully
      - **IDK why but in my test did not pan out**
    - `'django.core.mail.backends.smtp.EmailBackend'`
      - Specify that sends email via SMTP server
  - `EMAIL_USE_LOCALTIME`
    - Whether to send the SMTP Date header of email messages in the local time zone (True) or in UTC (False).
  - `EMAIL_TIMEOUT`
    - Specifies a timeout in seconds for blocking operations like the connection attempt.
  - `EMAIL_FILE_PATH`
    - The directory used by the file email backend to store output files.
  - `DEFAULT_FROM_EMAIL`
    - Default email address to use for various automated correspondence from the site manager(s). This doesn’t include error messages sent to ADMINS and MANAGERS; for that, see SERVER_EMAIL.
  - `SERVER_EMAIL`
    - The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
  - SMTP
    - `EMAIL_HOST`
      - host to use for sending email
    - `EMAIL_PORT`
      - use for the SMTP server defined in EMAIL_HOST
    - If either of these settings is empty, Django won’t attempt authentication for SMTP server.
      - `EMAIL_HOST_USER`
      - `EMAIL_HOST_PASSWORD`
- Database
  - `DATABASES`
    - A dictionary containing the settings for all databases
    - Must configure a default database
    - `ATOMIC_REQUESTS` to wrap each request into a transaction
    - `AUTOCOMMIT` Django manages transactions or you
    - `ENGINE`
      - `'django.db.backends.postgresql'`
      - `'django.db.backends.mysql'`
      - `'django.db.backends.sqlite3'`
      - `'django.db.backends.oracle'`
    - `HOST`
      - Empty string means localhost.
      - `'/var/run/mysql'` connect with socket
    - `NAME` is database name
    - `CONN_MAX_AGE`
      - lifetime of a database connection
      - seconds
    - `PASSWORD`
    - `PORT` empty string means the default port
    - `USER`
- `DEFAULT_FILE_STORAGE`
  - Default file storage class to be used for any file-related operations that don’t specify a particular storage system.
- CORS
  - `SECURE_CROSS_ORIGIN_OPENER_POLICY`
    - Default: `'same-origin'`
    -
- Timezone:
  - `USE_TZ`
  - `TIME_ZONE`
    - Default: `'America/Chicago'`
    - When `USE_TZ` is `False`, this is the time zone in which Django will store all datetimes. When `USE_TZ` is True, this is the default time zone that Django will use to display datetimes in templates and to interpret datetimes entered in forms.

# Routing

- `urlpatterns` should be a sequence of `path()` and/or `re_path()` instances.
- Point the root URLconf at the `polls.urls`, or whatever is the module's name.
  - `include('polls.url')`
    - Referencing other URLconfs.
    - Request comes, it chops off whatever part of the URL matched up to that point(Match to the defined string as endpoint) and sends the remaining string to the included URLconf(That newly created `polls/urls.py`) for further processing.
    - Reason behind the `include`:
      - Make it easy to plug-and-play URLs.
      - Since polls are in their own URLconf (`polls/urls.py`), they can be placed under `"/polls/"`, or under `"/fun_polls/"`, or under `"/content/polls/"`, or any other path root, and the app will still work.
        - TBH IDK what this section means
    - **You should always use `include()` when you include other URL patterns.**
      - `admin.site.urls` is the only exception to this.
  - `path()`
    - 4 arguments
      - 2 required:
        - `route`
          - A string that contains a URL pattern.
          - Django start from the first and goes down to the list
          - **Patterns don’t search `GET` and `POST` parameters**
            - I was stocked around 30min or I guess 1 hour on just this tiny data.
            - This is also right in DRF
          - **Patterns don’t search domain name.**
            - `https://www.example.com/myapp/`
            - `https://www.example.com/myapp/?page=3`
              - Both looks for URLconf `myapp/`
        - `view`
          - A matching pattern founded.
            - Call the specified view function with an `HttpRequest` object as the first argument
              - Any "captured" values from the route as keyword arguments.
      - 2 optional:
        - `kwargs`
          - Arbitrary keyword arguments can be passed in a dictionary to the target view
          - TBH IDK what it means
        - `name`
          - Naming your URL
          - Refer to URL unambiguously from elsewhere in Django
            - Redirect to another endpoint with their name
          - To make global changes to the URL patterns of your project while only touching a single file.
          - I guess it means we can do change our endpoints needless to change our codes.
- URL Dispatcher
  - No framework limitations, Do what you want. 100% freedom.
  - ## [Cool URIs don’t change, by World Wide Web creator Tim Berners-Lee](https://www.w3.org/Provider/Style/URI)
  - Create a Python module informally called a `URLconf` (URL configuration). A mapping between URL path expressions to Python functions (your views).
  - # How Django processes a request
    - User requests a page
    - Django determines root `URLconf` module to use. Usually `ROOT_URLCONF` setting
    - Django loads Python module and looks for the variable `urlpatterns`.
    - Django goes up to down in URL patterns, stops at the first one that matches the requested URL
    - Django imports and calls the given view with these args:
      - An instance of `HttpRequest`.
      - URL path parameters (`/users/1`) and URL parameters (`/users?page=1`)
    - **No** URL pattern matches, Django invokes an appropriate error-handling view
- Different ways to route
  - `path('', TemplateView.as_view(template_name='views/main.html')),`
    - Here we use Django power. We are saying that you figure it out how your should return this html page
  - **No** need to add a leading slash, because every URL has that. `/articles` and `article` is the same in this example:
    ```py
    from django.urls import path
    from . import views
    urlpatterns = [
        path('articles/2003/', views.special_case_2003),
        path('articles/<int:year>/', views.year_archive),
        path('articles/<int:year>/<int:month>/', views.month_archive),
        path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
    ]
    ```
  - Path converters:
    - `str` default convertor
    - `int` zero or any positive integer.
    - `slug`
      - ASCII letters
      - numbers
      - the hyphen and underscore characters.
      - `building-your-1st-django-site`
    - `uuid`
      - There was a warning but I do not understand it. Please read Doc
    - `path`
      - I do not get this one at all. READ doc.
  - Here we used function based view
    - `path('funky', views.funky),`
      - Here we pass a function for this route
    - `path('rest/<int:guess>', views.rest),`
      - To capture a value from the URL, use angle brackets.
      - This captured value includes a converter type
      - Here we used a URL path parameter
      - It will convert it automatically to `int`
  - Here we use class base view:
    - `path('main', views.MainView.as_view()),`
    - `path('remain/<slug:guess>', views.RestMainView.as_view()),`
      - `slug` is a kind of string but with specific meaning
    - `as_view` converts our class to view

# Views

- As we said Django look into `urls.py` and select proper `views.py`
- Here we do:
  - Process incoming request
  - Do database queries
  - Generate response where it can be html, json, string, etc
- How Django process HTTP incoming request:
  - `http://doman.name/app_name/view_within_app_name`
  - `http://doman.name/app_name/view_within_app_name/24` which 24 is URL path parameter
  - `GET http://doman.name/app_name/view_within_app_name?guess=42`
- We have access to Request object and Response Object in the views:
  1. A page is requested
  2. Django creates an `HttpRequest` object that contains request metadata.
  3. Django loads the appropriate view, passing the `HttpRequest` as the first argument to the view function.
  4. Each view is responsible for returning an `HttpResponse` object.
- [Learn more about req and res objects](https://docs.djangoproject.com/en/4.0/ref/request-response)
- `HttpRequest`
  - Instantiates a `QueryDict` object based on query_string.
    ```py
    QueryDict('a=1&a=2&c=3')
    # <QueryDict: {'a': ['1', '2'], 'c': ['3']}>
    ```
  - Attributes:
    - `req.GET['guess']`
      - **Do not do `req.GET.guess`. It is wrong, Python throw error**
      - A dictionary-like object with all given HTTP GET parameters.
      - Catches Query string named `guess`.
      - You can use `escape` utility function to prevent XSS
        ```py
        from django.utils.html import escape
        from django.http.request import HttpRequest
        from django.http.response import HttpResponse
        def no_xss(req: HttpRequest) -> HttpResponse:
            return HttpResponse(f"<h1>{escape(req.GET['guess'])}</h1>")
        ```
    - `req.scheme`
      - http or https (usually)
    - `req.body`
      - Raw HTTP request body as a bytestring.
      - For processing conventional **form data**, use `req.POST`.
    - `req.path`
      - the full path to the requested page
      - "/music/bands/the_beatles/"
      - Alternative: `req.get_full_path()`
    - `req.method`
      - HTTP verb
      - guaranteed to be uppercase
    - `req.POST`
      - A dictionary-like object with all given HTTP POST parameters, form data.
      - Files are not in here. Check the `req.FILES`
    - `req.FILES`
      - A dictionary-like object with all uploaded files.
      - Each key in `FILES` is the name from the `<input type="file" name="">`.
      - It has file if:
        - HTTP verb be `POST`
        - And `enctype="multipart/form-data"`
    - `req.META`:
      - A dictionary containing all available HTTP headers.
      - Here is a list of possible useful values:
        - `CONTENT_TYPE`
        - `HTTP_USER_AGENT`
        - `REMOTE_ADDR`
          - The IP address of the client.
          - Alternative: `req.get_port()`
  - `HttpResponse`:
    - `HttpResponse` sub classes:
      - `HttpResponseRedirect`:
        - status code: 302 (found)
        - Redirect user to another page
          ```py
          from django.utils.html import escape
          from django.http.request import HttpRequest
          from django.http.response import HttpResponseRedirect
          # Please note that this ": int" do not convert the string into int
          # It is done by django and because we did:
          # path('rest/<int:guess>', views.rest)
          def rest(req: HttpRequest, guest: int) -> HttpResponseRedirect:
              return HttpResponseRedirect("https://www.linkedin.com/in/kasir-barati/")
          ```
      - `HttpResponsePermanentRedirect`
        - status code: 301
      - `HttpResponseNotModified`
        - status code: 304
      - `HttpResponseBadRequest`
        - status code: 400
      - `HttpResponseNotFound`
        - status code: 404
      - `HttpResponseForbidden`
        - status code: 403
      - `HttpResponseNotAllowed`
        - HTTP verb is not valid
        - status code: 405
      - `HttpResponseGone`
        - status code: 410
      - `HttpResponseServerError`
        - status code: 500
    - `StreamingHttpResponse`:
      - Django is designed for short-lived requests
      - tie a worker process
      - poor performance.
      - Sub classes:
        - `FileResponse`:
          - optimized for binary files.
          - streams the file out in small chunks.
            ```py
            from django.http import FileResponse
            response = FileResponse(open('myfile.png', 'rb'))
            ```
            The file will be closed automatically, so don’t open it with a context manager.
- Getting URL path parameters
  ```py
  from django.utils.html import escape
  from django.http.request import HttpRequest
  from django.http.response import HttpResponse
  # Please note that this ": int" do not convert the string into int
  # It is done by django and because we did:
  # path('rest/<int:guess>', views.rest)
  def rest(req: HttpRequest, guest: int) -> HttpResponse:
      return HttpResponse(f"<h1>{escape(guess)}</h1>")
  ```
- Templates:
  - Mostly HTML
  - Pass the request object, HTML file path, and lastly data
    ```py
    from django.views import View
    from django.shortcuts import render
    from django.http.request import HttpRequest
    class GameView(View):
        def get(self, req: HttpRequest, guess: int) -> HttpResponse:
            data = { "user_guess": guess }
            return render(req, 'polls/user_guess.html', data)
    ```
    - The important part is that you have to put your templates in another directory with the same name as our app. This is a must.
      - `my-touch polls/templates/polls/user_guess.html`
        - **That `polls` duplication is required**.
  - We have many template engines
    - ## [In the name of the father, the son, and the holy ghost, READ doc for Christ sake](https://docs.djangoproject.com/en/4.0/topics/templates/)
    - substitution: `{{ user_guess|safe }}`
      - We say that do not escape this string and let browser to interpreter it as a html/js/css
    - calling code: `{% author.get_books() %}`
    - conditions:
      ```
      {% if user_guess > 100 %}
      {% endif %}
      ```
    - loops:
      ```
      {% for user in users %}
      <h1>Name: {{ user.name }}</h1>
      <h5>Name length: {{ user.name|length }}</h5>
      {% endif %}
      ```
    - blocks:
      ```
      {% block content %}
      {% endblock %}
      ```
    - `{# this won't be rendered #}`
  - Template inheritance:
    - navbar, etc.
    - DRY principle
    - How to use?
      - `{% block content %}{% endblock %}` in the `base.html`
      - `{% extends "polls/base.html" %}` in the `user_guess.html`
  - Linking templates to each other:
    - We use specified `name` in `urls.py` instead of hard coded strings
- Function-based views
  - Lower level
  - Here we have to check whether we got get request or post request
- [Class-based views](https://docs.djangoproject.com/en/4.0/ref/class-based-views):
  - **_READ Doc for sure_**
  - Here we have many features
  - Understand HTTP verbs.
  - We have a deep inheritance in Views. Mixins and Generic class-based views will help us in those cases that the default one cannot fulfill our needs.
  - `django.views.generic.base.View`
    - The master class-based base view.
    - All other class-based views inherit from this base class.
    - It isn’t strictly a generic view and thus can also be imported from `django.views`.
- Generic views:
  - DRY
  - In CRUD we do not wanna rewrite tons of code again and again
  - Keep code consistent
  - Less line of code means less :bug:

# Models

- [Django official doc](https://docs.djangoproject.com/en/4.0/topics/db/queries/)
- [Related lecture link](https://www.dj4e.com/lectures/DJ-02-Model-Single.txt)
- Each model has one [`Manager`](https://docs.djangoproject.com/en/4.0/topics/db/managers/#django.db.models.Manager), and it’s called `objects` by default.
  - Access it directly via the model class, like so:
    - `User.objects`
- An intuitive system to represent database-table data in Python objects
  - Extends/Inheritance from `Model` which is in the `django.db.models`
  - Define field types in `modes.py`
  - A model class represents a database table
    - An instance of class represents a particular record
- `filter` create the `where` clause for us
- We have ORM in place. You do not need to install ORM
  - Abstract layer on top SQL database management systems
  - But why ORM?
    - Just python not SQL
    - More readily change your database
    - A powerful built-in migration system
    - Automatic form generation and validation
- How many query executed against database:
  ```py
  q = Article.objects.filter(headline__startswith="What")
  q = q.filter(pub_date__lte=datetime.date.today())
  q = q.exclude(body_text__icontains="food")
  print(q)
  ```
  - Though **this looks like three database hits**, in fact **it hits the database only once**, at the last line (`print(q)`). In general, the results of a `QuerySet` ain't fetched from the database until you "ask" for them. When you use the `QuerySet` it is evaluated by accessing the database.
- **CRUD**
  - Create:
    - `u = User(name='Kristen', email='kf@umich.edu')`
      - It is not saved in db, yet. `u.save()`
        - `.save` has no return value.
      - You can alternatively use `User.create()` to create and save the new record at once.
  - Read:
    - A list of options:
      - contains
      - icontains
      - startswith
      - endswith
      - iendswith
      - istartswith
    - Automatic join:
      ```py
      class Blog(models.Model):
          name = models.CharField(max_length=100)
          tagline = models.TextField()
          def __str__(self):
              return self.name
      class Entry(models.Model):
          blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
          headline = models.CharField(max_length=255)
          body_text = models.TextField()
          pub_date = models.DateField()
          mod_date = models.DateField(default=date.today)
          authors = models.ManyToManyField(Author)
          number_of_comments = models.IntegerField(default=0)
          number_of_pingbacks = models.IntegerField(default=0)
          rating = models.IntegerField(default=5)
          def __str__(self):
              return self.headline
      Entry.objects.filter(blog__name='Beatles Blog')
      ```
    - JSON fields:
      ```py
      class Dog(models.Model):
          name = models.CharField(max_length=200)
          data = models.JSONField(null=True)
          def __str__(self):
              return self.name
      Dog.objects.create(name='Rufus', data={
          'breed': 'labrador',
          'owner': {
              'name': 'Bob',
              'other_pets': [{
                  'name': 'Fishy',
              }],
          },
      })
      Dog.objects.filter(data__owner__name='Bob')
      ```
    - These queries return an `QuerySet`
      - A `QuerySet` represents a collection of objects from database.
      - `QuerySet` equates to a `SELECT` statement
      - Each `QuerySet` contains a cache to minimize database access.
    - `User.objects.values()`
    - `User.objects.values().order_by('-name')`
    - `User.objects.filter(email='csev@umich.edu').values()`
      - Add a `WHERE` clause to return a narrow result.
        - **Caution**
          ```py
          Blog.objects.exclude(
              entry__headline__contains='Lennon',
              entry__pub_date__year=2008,
          )
          ```
          This query would exclude blogs that contain "Lennon" in the headline or published in 2008. If you need that you should perform 2 query:
          ```py
          Blog.objects.exclude(
              entry__in=Entry.objects.filter(
                  headline__contains='Lennon',
                  pub_date__year=2008,
              ),
          )
          ```
        - Compare the value of a model field with another field on the same model:
          - `F expressions`
          - Author’s name is the same as the blog name
            ```py
            from django.db.models import F
            Entry.objects.filter(authors__name=F('blog__name'))
            ```
    - Get by ID:
      ```py
      Blog.objects.get(id__exact=14) # Explicit form
      Blog.objects.get(id=14) # __exact is implied
      Blog.objects.get(pk=14) # pk implies id__exact
      Blog.objects.filter(pk__in=[1,4,7]) # With id 1, 4 and 7
      Blog.objects.filter(pk__gt=14) # id > 14
      ```
    - `Article.objects.filter(headline__startswith="What")`
      - Pass an invalid keyword argument, it will raise `TypeError`.
      - If there should be only one object that matches your query use `get()`
        - `User.objects.get(pk=1)`
        - "exact" and "iexact" match:
          - iexact is just case-insensitive
          - `Blog.objects.get(slug__exact='some-blog') # Explicit form`
          - `Blog.objects.get(slug='some-blog') # __exact is implied`
            - `WHERE id = 'some-blog'`
        - It will raise:
          - `DoesNotExist` exception if there was no record
          - `MultipleObjectsReturned` exception if there were more than one record
    - `LIMIT` and `OFFSET` clauses.
      - `User.objects.all()[:5]` LIMIT = 5
      - `User.objects.all()[5:10]` OFFSET = 5, and LIMIT = 5
  - Update:
    - `User.objects.filter(email='csev@umich.edu').update(name='Charles')`
      - `filter` is a limiting clause such as `WHERE` or `LIMIT`.
      - Returns a new `QuerySet` containing objects that match the given lookup parameters.
      - Always give you a `QuerySet`
  - Delete:
    - `delete()`
      - Deletes the object and returns the number of objects deleted and a dictionary with the number of deletions per object type.
    - `User.objects.exclude(email='ted@umich.edu').delete()`
      - Returns a new `QuerySet` containing objects that do not match the given lookup parameters. and delete them
    - It does SQL constraint `ON DELETE CASCADE`
      - Customizable via the `on_delete` argument to the `ForeignKey`.

# Objects in Python

- Everything is object
  - String is an object
- Why OOP:
  - Isolation
  - DRY
  - Extensibility
- Class is an abstract concept
- Instances are real objects
- Class have:
  - property
  - methods
- Object lifecycle:
  - `constructor` or in python `__init__`
    - Create instance of the class
  - `destructor` or in python `__del__`
    - When the instance going to be deleted
- Inheritance:
  - Here we have code reuse

# Forms in Django

- HTTP verbs:
  - `POST` create or modify data
  - `GET` reading data
- CSRF protection:
  - Generate a token
  - Put it in the generated form in a hidden tag
  - Check if it is provided and its value is correct
  - Now rogue server cannot pretend that it is the legit server. Because it does not have access to our server.
  - In Django we are protected by default but we need to implement it:
    - `@csrd_exempt` says to the Django that I do not handle CSRF. Please do not bother me right now. I will implement it.
    - ### Implement CSRF
      - Just use `{% csrf_token %}` in your html file. It does its job. Just remember to enable the CSRF token if it is disabled.
- :warning:**Never sends an HtML page in response to a POST request**:warning:
  - Why? Because if user press f5 - Reload the page - browser tries to resend the previous POST request. Assume you've done a money transfer to someone. It's gonna duplicate. Obviously browser ask permission from user. But users do not know anything about it. So most of time they just say yes do it.
  - Solution:
    - Redirect user
    - [Note to enable your django app's sessions](https://docs.djangoproject.com/en/4.0/topics/http/sessions/#:~:text=Enabling%20sessions&text=To%20enable%20session%20functionality%2C%20do,sessions.)
    - If this error raised: `no such table: django_session`
      - `python manage.py makemigrations`
      - `python manage.py migrate`
      - Here is why: Probably you never did a `makemigrations` or you already have done it. But you did `migrate`. Or the last one is that you delete your database and now database is empty, so you need to do `migrate` again.

# Authentication in Django

- Django is battery included:
  - Handles both authentication and authorization
  - Built on top of sessions
  - But you need 3rd party packages for:
    - Password strength checking
    - Throttling of login attempts
    - OAuth
    - Object-level permissions
  - Bundled as a Django contrib module in `django.contrib.auth`
- Auth system buts and bolts:
  - Users
    - `from django.contrib.auth.models import User`
    - **Set up a custom user model when starting an actual project. Do not use this one**
  - Groups
    - `from django.contrib.auth.models import Group`
  - Permissions
  - A configurable password hashing system
  - Forms and view tools for logging in users, or restricting content
  - A pluggable backend system
- The primary attributes of the default user are ([doc](https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#django.contrib.auth.models.User)):
  - `username`
  - `password`
  - `email`
  - `first_name`
  - `last_name`
- Change password ways:
  - CLI: `python manage.py changepassword *username*`
  - Programmatically: `User.objects.get(username='john').set_password('new password')`
  - Admin panel
  - User panel
- [Django Tutorial Part 8: User authentication and permissions](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication)
  - Add `django.contrib.auth` and `'django.contrib.contenttypes'` to your installed apps.
    - First one Contains the core of the authentication framework, and its default models.
    - Last one is the Django content type system, which allows permissions to be associated with models you create.
  - `SessionMiddleware` and `AuthenticationMiddleware` in `middleware` section
  - `path('accounts/', include('django.contrib.auth.urls')),`
  - Get the url with `reverse('login')` and `reverse('logout')`
  - Create authentication pages to handle login, log out, and password management "out of the box".
  - This includes a URL mapper, views and forms, **but it does not include the templates — we have to create our own!**
    - I was stocked right here. I thought fo hours why it does not show me anything
  - Shared login behavior and available across the whole site.
  - If you've follow me along you should get this error **django.template.exceptions.TemplateDoesNotExist: registration/login.html**
    while sending request to the `http://127.0.0.1:8000/accounts/login/`
    - To vanish this error:
      - Create a registration directory on the search path and then add the `login.html` file.
      - It is also possible that your project name is not appropriate for a python project.
        - After renaming to a valid director name do not forget to remove the old venv and create a new one. [ref](https://stackoverflow.com/a/72850572/8784518)
      - The path to templates is not correct:
        - `/home/kasir/go-back-to-score-one-in-learning-django/1_web_app_technologies_and_django/first_django_app/go_back_start_again/go_back_start_again/templates/registration/login.html`
          - For when I was using `os.path.join(os.path.dirname(__file__), 'templates'),`
        - `/home/kasir/go-back-to-score-one-in-learning-django/1_web_app_technologies_and_django/first_django_app/venv/lib/python3.10/site-packages/django/contrib/admin/templates/registration/login.html`
          - For when I did not specify any path to templates
      - At last you should create the `base_generic.html` in your share templates directory
  - Now if you try to login you face with yet another error, `Page not found (404)` because obviously as we were responsible to define our login page, we are incharge to create profile page too
    - By default, Django expects that upon logging in you will want to be taken to a profile page.
    - However we can change this behavior via `LOGIN_REDIRECT_URL = '/'` configuration.
    - But we have to at then end of the day create this page too
  - Now its time to create logout page: `my-touch templates/registration/logged_out.html`
  - Password reset form
    - email user a reset link
    - create forms to get the user's email address
    - `my-touch templates/registration/password_reset_form.html`
    - `my-touch templates/registration/password_reset_done.html`
    - `my-touch templates/registration/password_reset_email.html`
      - The email your app will send to the user
    - `my-touch templates/registration/password_reset_confirm.html`
    - `my-touch templates/registration/password_reset_complete.html`
- To restrict access to logged-in users in your class-based views derive from `LoginRequiredMixin`.
  - Same as using `@login_required` decorator
  - Specify alternative location to redirect user to it if not authenticated (`login_url`)
  - A URL parameter name instead of "next" to insert the current absolute path (`redirect_field_name`).
