import json

from django.http import JsonResponse
from django.views import View
from django import forms

from core.models import Location, User, Visit


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
        if form.is_valid():
            instance = form.save()
            response_data = {
                'status': 'OK',
                'data': instance.as_json()
            }
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

    form_class = CreateVisitForm
