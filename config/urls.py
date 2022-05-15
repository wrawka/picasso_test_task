from django.contrib import admin
from django.urls import path

from picasso_parser.views import index, parse


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name='index'),
    path("parse", parse, name='parse')
]
