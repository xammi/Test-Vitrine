from django.conf.urls import url
from core.views import UserView, LocationView, VisitView

urlpatterns = [
    url('^user/', UserView.as_view(), name='user'),
    url('^location/', LocationView.as_view(), name='location'),
    url('^visit/', VisitView.as_view(), name='visit'),
]
