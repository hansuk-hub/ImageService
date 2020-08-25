from django.urls import path, include
from . import views
from . import makehtml


urlpatterns = [
     path('test/', views.test),
     path('make-html/', makehtml.start)
]