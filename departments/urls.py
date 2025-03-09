from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.departementsHandler, name='departementsHandler'),
    path('course/', view=views.coursesHandler, name='coursesHandler')
]