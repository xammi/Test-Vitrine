from django.http import HttpResponse
from django.views import View


class UserView(View):
    http_method_names = ['create']

    def create(self, request, *args, **kwargs):
        return HttpResponse(status=200)


class LocationView(View):
    http_method_names = ['create']

    def create(self, request, *args, **kwargs):
        return HttpResponse(status=200)


class VisitView(View):
    http_method_names = ['create']

    def create(self, request, *args, **kwargs):
        return HttpResponse(status=200)
