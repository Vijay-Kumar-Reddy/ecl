from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("",views.index, name="home"),
    path("cigars/",views.cigar_collection, name="cigars"),
    path("bar_and_cocktail/",views.bar_and_cocktail, name="bar_and_cocktail"),
    path("liquor/",views.liquor_collection, name="liquor"),
    path("bar_menu/",views.bar_menu, name="bar_menu"),
    path("event_page/",views.event_page, name="event_page"),
    path("event/<int:event_id>/gallery/", views.event_gallery, name="event_gallery"),

]
