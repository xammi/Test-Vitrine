from django.conf.urls import url

from .views import UserView, LocationView, VisitView, IndexView

urlpatterns = [
    url('^$', IndexView.as_view(), name='home'),

    url('^user/$', UserView.as_view(), name='user'),
    url('^location/$', LocationView.as_view(), name='location'),
    url('^visit/$', VisitView.as_view(), name='visit'),
]
