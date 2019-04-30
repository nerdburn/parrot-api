from django.urls import path

from . import views

urlpatterns = [
    path('import', views.FetchView.as_view(), name='import')
]