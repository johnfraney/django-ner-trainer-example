"""ner_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from ner_trainer import urls as ner_trainer_urls
from . import views

urlpatterns = [
    path('entities/', views.EntityList.as_view(), name='entity-list'),
    path('phrases/', views.PhraseList.as_view(), name='phrase-list'),
    path('phrases/untagged/', views.PhraseListUntagged.as_view(), name='phrase-list-untagged'),
    path('phrases/<int:pk>/', views.PhraseDetail.as_view(), name='phrase-detail'),
    path('phrases/<int:pk>/set-entities/', views.set_phrase_entities, name='phrase-set-entities'),
    path('api/', include(ner_trainer_urls)),
    path('admin/', admin.site.urls),
]
