from django.views.generic import ListView
from django.views.generic import View
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import render 
from django.contrib.auth.mixins import LoginRequiredMixin
# from datetime import datetime
from django.utils import timezone
from .models import Apple


# Create your views here.
class ListApple(ListView):
    model = Apple
    paginate_by = 100  # if pagination is desired

    # This name is preserved
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        # context['now'] = datetime.now()
        """
        - datetime.now()
        I guess we do not like this one too much
        Returns local time: datetime.datetime(2022, 7, 3, 18, 40, 31, 441670)
        - timezone.now()
        Read USE_TZ and generate time based on this setting
        """
        return context


class CsrfProtectedForm(View):
    # This "get" specify the HTTP verb
    # def get(self, req: HttpRequest):
    #     return render(req, 'gview/csrf_protected_form.html')
    
    # def get(self, req: HttpRequest):
    #     # <flash-message>
    #     guessed_number = req.session.get('guessed_number', False)
    #     if guessed_number != False:
    #         del(req.session['guessed_number'])
    #     context = {"guessed_number": guessed_number}
    #     # </flash-message>

    #     return render(req, 'gview/csrf_protected_form.html', context)

    def get(self, req: HttpRequest):
        # <flash-message>
        guessed_number = req.session.get('guessed_number', False)
        if guessed_number != False:
            del(req.session['guessed_number'])
        context = {
            "guessed_number": guessed_number,
            "logout": reverse('logout'),
            "login": reverse('login'),
        }
        # </flash-message>

        return render(req, 'gview/csrf_protected_form.html', context)
    
    # This "post" specify the HTTP verb
    # def post(self, req: HttpRequest):
    #     guess = req.POST.get('guess')
    #     context = {"guess": guess}
    #     return render(req, 'gview/csrf_protected_form.html', context)

    def post(self, req: HttpRequest):
        guess = req.POST.get('guess')
        req.session['guessed_number'] = guess
        return redirect(req.path)


class ProtectedView(LoginRequiredMixin, View):
    login_url = 'login'
    # No effect. IDK how I should configure it. I do not care too much about it right now
    # redirect_field_name = 'redirect_to'
    
    def get(self, req: HttpRequest) -> HttpResponse:
        return HttpResponse('I am protected')

