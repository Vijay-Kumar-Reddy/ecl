from django.contrib import admin
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
    EventImage,
    EventVideo,
)

# ======================================================
#  MODEL ADMINS
# ======================================================

# ---------- BANNER ----------
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_active", "button_link"]
    list_filter = ["is_active"]
    ordering = ["order"]
    search_fields = ["title", "subtitle"]


# ---------- CIGAR ----------
@admin.register(Cigar)
class CigarAdmin(admin.ModelAdmin):
    list_display = ("name", "origin", "price", "order", "is_active")
    list_editable = ("price", "order", "is_active")
    search_fields = ("name", "origin")
    ordering = ("order",)


# ---------- CIGAR OFFERS ----------
@admin.register(CigarOffer)
class CigarOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "discount_percent", "apply_to_all", "is_active", "order")
    list_editable = ("discount_percent", "apply_to_all", "is_active", "order")
    filter_horizontal = ("cigars",)
    ordering = ("order",)


# ---------- DRINKS ----------
@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    ordering = ("order",)


# ---------- LIQUOR ----------
@admin.register(Liquor)
class LiquorAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    ordering = ("order",)


# ---------- BAR CATEGORY + ITEMS ----------
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


# ---------- GALLERY IMAGE (HOME PAGE GALLERY) ----------
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")


# ======================================================
#  EVENT + EVENT GALLERY INLINES (FINAL VERSION)
# ======================================================

class EventImageInline(admin.TabularInline):
    model = EventImage
    fields = ["image", "caption", "order"]
    extra = 1
    ordering = ["order"]


class EventVideoInline(admin.TabularInline):
    model = EventVideo
    fields = ["video", "caption", "order"]
    extra = 1
    ordering = ["order"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "is_active")
    list_filter = ("is_active", "date")
    search_fields = ("title", "location", "description")
    ordering = ("-date",)
    inlines = [EventImageInline, EventVideoInline]   # <-- THIS SHOWS GALLERY IN ADMIN


