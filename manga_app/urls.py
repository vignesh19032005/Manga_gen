from django.urls import path
from . import views

app_name = 'manga_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_manga, name='generate'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('panels/', views.panels, name='panels'),
    path('generate_panels/', views.generate_panels, name='generate_panels'),
]
