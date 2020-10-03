from django.urls import path, include
from . import views

app_name = 'competition'

urlpatterns = [
    path("", views.CompetitionPage.as_view(), name="home_page"),
    path("amongus/<title>", views.CompetitionPage.as_view(), name="amongus")
]