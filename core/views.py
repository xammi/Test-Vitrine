import json
from datetime import datetime

import pytz
from django.db import transaction
from django.http import JsonResponse
from django.views import View
from django import forms

from core.models import Location, User, Visit


cache_limit = 500
insert_cache = []


class JsonCreateView(View):
    http_method_names = ['post']
    form_class = None

    def extract_params(self, request):
        if request.POST:
            return request.POST
        body = {}
        if request.body:
            try:
                body = json.loads(request.body.decode("utf-8"))
            except Exception:
                return {}
        return body

    def post(self, request, *args, **kwargs):
        params = self.extract_params(request)
        form = self.form_class(params)
        flush = request.POST.get('flush', 'False')
        if form.is_valid():
            instance = form.save(commit=False)
            insert_cache.append(instance)
            if flush == 'False' and len(insert_cache) < cache_limit:
                response_data = {'status': 'WAIT'}
            else:
                ids = []
                with transaction.atomic():
                    for instance in insert_cache:
                        try:
                            instance.save()
                            ids.append(instance.id)
                        except Exception:
                            pass
                    insert_cache.clear()
                response_data = {'status': 'OK', 'data': ids}
        else:
            response_data = {
                'status': 'ERROR',
                'errors': {k: v for k, v in form.errors.items()}
            }
        return JsonResponse(response_data, safe=False)


class UserView(JsonCreateView):
    """
    curl -X post 'http://127.0.0.1:8000/user/' -H 'Content-Type: application/json' -d '{"email": "max_3@mail.ru", "first_name": "Максим", "last_name": "Кисленко"}'
    """

    class CreateUserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['email', 'first_name', 'last_name', 'birth_date']

    form_class = CreateUserForm


class LocationView(JsonCreateView):
    """
    curl -X post 'http://127.0.0.1:8000/location/' -H 'Content-Type: application/json' -d '{"country": "Россия", "city": "Москва", "place": "Москва-сити"}'
    """

    class CreateLocationForm(forms.ModelForm):
        class Meta:
            model = Location
            fields = ['country', 'city', 'place']

    form_class = CreateLocationForm


class VisitView(JsonCreateView):
    """
    curl -X post 'http://127.0.0.1:8000/visit/' -H 'Content-Type: application/json' -d '{"user_id": 1, "location_id": 1}'
    """

    class CreateVisitForm(forms.ModelForm):
        class Meta:
            model = Visit
            fields = ['location', 'user', 'visited_at']

        def full_clean(self):
            self.cleaned_data = {
                'user_id': int(self.data['user']),
                'location_id': int(self.data['location']),
                'visited_at': datetime.strptime(self.data['visited_at'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC),
            }

        def save(self, commit=True):
            instance = Visit(user_id=self.cleaned_data['user_id'],
                             location_id=self.cleaned_data['location_id'],
                             visited_at=self.cleaned_data['visited_at'])
            if commit:
                instance.save()
            return instance

    form_class = CreateVisitForm
