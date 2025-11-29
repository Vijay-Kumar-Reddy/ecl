from django.contrib import admin
from django.urls import path
from django.utils import timezone
from django.template.response import TemplateResponse

from .models import (
    Banner,
    Cigar,
    CigarOffer,
    Drink,
    Liquor,
    BarCategory,
    BarItem,
    Event,
    GalleryImage,
)



# ======================================================
#  MODEL ADMINS
# ======================================================

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_active", "button_link"]
    list_filter = ["is_active"]
    ordering = ["order"]
    search_fields = ["title", "subtitle"]


@admin.register(Cigar)
class CigarAdmin(admin.ModelAdmin):
    list_display = ("name", "origin", "price", "order", "is_active")
    list_editable = ("price", "order", "is_active")
    search_fields = ("name", "origin")
    ordering = ("order",)


@admin.register(CigarOffer)
class CigarOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "discount_percent", "apply_to_all", "is_active", "order")
    list_editable = ("discount_percent", "apply_to_all", "is_active", "order")
    filter_horizontal = ("cigars",)
    ordering = ("order",)


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    ordering = ("order",)


@admin.register(Liquor)
class LiquorAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    ordering = ("order",)


class BarItemInline(admin.TabularInline):
    model = BarItem
    extra = 1


@admin.register(BarCategory)
class BarCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    inlines = [BarItemInline]


@admin.register(BarItem)
class BarItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active", "order")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    list_editable = ("order", "is_active")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "location", "is_active"]
    list_filter = ["is_active", "date"]
    search_fields = ["title", "location", "description"]
    ordering = ["-date"]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
