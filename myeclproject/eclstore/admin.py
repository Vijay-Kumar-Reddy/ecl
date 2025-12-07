from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd

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
#                 BANNER ADMIN
# ======================================================

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "order",
        "expiry_date",
        "status_colored",
    ]

    list_filter = ["is_active"]
    search_fields = ["title", "subtitle"]
    ordering = ["order"]

    def status_colored(self, obj):
        color = "green" if obj.is_active else "red"
        text = "ACTIVE" if obj.is_active else "EXPIRED"
        return format_html(f"<b style='color:{color}'>{text}</b>")

    status_colored.short_description = "Status"

    def expiry_date(self, obj):
        if not obj.display_duration_days:
            return "— Unlimited —"
        return obj.start_date + timezone.timedelta(days=obj.display_duration_days)

    expiry_date.short_description = "Expires On"


# ======================================================
#                     CIGAR ADMIN (WITH EXCEL UPLOAD)
# ======================================================

@admin.register(Cigar)
class CigarAdmin(admin.ModelAdmin):

    change_list_template = "admin/cigar_change_list.html"

    list_display = ("name", "origin", "price", "order", "is_active")
    list_editable = ("price", "order", "is_active")
    search_fields = ("name", "origin")
    ordering = ("order",)

    # Add custom URL for Excel upload
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-excel/", self.upload_excel, name="cigar_upload_excel"),
        ]
        return custom_urls + urls

    # Excel Upload Handler
    def upload_excel(self, request):
        if request.method == "POST":
            excel_file = request.FILES.get("excel_file")

            if not excel_file:
                messages.error(request, "Please upload a valid Excel file.")
                return redirect("admin:cigar_upload_excel")

            try:
                df = pd.read_excel(excel_file)
                df.columns = df.columns.str.lower()

                created_count = 0
                updated_count = 0
                skipped_count = 0

                for _, row in df.iterrows():
                    name = str(row.get("name", "")).strip()
                    price = row.get("price", None)

                    if not name:
                        continue

                    cigar, created = Cigar.objects.get_or_create(name=name)

                    if created:
                        created_count += 1
                        if pd.notna(price):
                            cigar.price = price
                        cigar.save()

                    else:
                        if pd.notna(price):
                            cigar.price = price
                            cigar.save()
                            updated_count += 1
                        else:
                            skipped_count += 1

                messages.success(
                    request,
                    f"Upload Complete! Created: {created_count}, Updated: {updated_count}, Skipped: {skipped_count}"
                )
                return redirect("admin:eclstore_cigar_changelist")

            except Exception as e:
                messages.error(request, f"Error reading file: {e}")
                return redirect("admin:cigar_upload_excel")

        return render(request, "admin/cigar_upload.html")


# ======================================================
#                     CIGAR OFFERS
# ======================================================

@admin.register(CigarOffer)
class CigarOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "discount_percent", "apply_to_all", "is_active", "order")
    list_editable = ("discount_percent", "apply_to_all", "is_active", "order")
    filter_horizontal = ("cigars",)
    ordering = ("order",)


# ======================================================
#                     DRINKS
# ======================================================

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    ordering = ("order",)


# ======================================================
#                     LIQUOR (WITH EXCEL UPLOAD)
# ======================================================

@admin.register(Liquor)
class LiquorAdmin(admin.ModelAdmin):

    change_list_template = "admin/liquor_change_list.html"

    list_display = ("name", "category", "price", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    ordering = ("order",)

    # Map category labels → model keys
    CATEGORY_MAP = {
        "Whiskey": "whiskey",
        "Rum": "rum",
        "Vodka": "vodka",
        "Gin": "gin",
        "Tequila": "tequila",
        "Wine": "wine",
        "Other": "other",
    }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-excel/", self.upload_excel, name="liquor_upload_excel"),
        ]
        return custom_urls + urls

    def upload_excel(self, request):
        if request.method == "POST":
            excel_file = request.FILES.get("excel_file")

            if not excel_file:
                messages.error(request, "Please upload a valid Excel file.")
                return redirect("admin:liquor_upload_excel")

            try:
                df = pd.read_excel(excel_file)
                df.columns = df.columns.str.lower()

                required_cols = {"name", "category", "price", "description"}
                if not required_cols.issubset(set(df.columns)):
                    messages.error(request, "Excel must contain: name, category, price, description.")
                    return redirect("admin:liquor_upload_excel")

                created_count = 0
                updated_count = 0
                skipped_count = 0

                for _, row in df.iterrows():
                    name = str(row.get("name", "")).strip()
                    category_label = str(row.get("category", "")).strip()
                    price = row.get("price", None)
                    description = row.get("description", None)

                    # Skip empty name rows
                    if not name:
                        continue

                    # Validate category label
                    if category_label not in self.CATEGORY_MAP:
                        skipped_count += 1
                        continue

                    category_key = self.CATEGORY_MAP[category_label]

                    liquor, created = Liquor.objects.get_or_create(name=name)

                    if created:
                        created_count += 1
                        liquor.category = category_key
                        if pd.notna(price): liquor.price = price
                        if pd.notna(description): liquor.description = description
                        liquor.save()

                    else:
                        updated = False

                        # Smart update (Option 1)
                        liquor.category = category_key

                        if pd.notna(price):
                            liquor.price = price
                            updated = True

                        if pd.notna(description) and str(description).strip():
                            liquor.description = description
                            updated = True

                        if updated:
                            liquor.save()
                            updated_count += 1
                        else:
                            skipped_count += 1

                messages.success(
                    request,
                    f"Liquor upload complete! Created: {created_count}, Updated: {updated_count}, Skipped: {skipped_count}"
                )
                return redirect("admin:eclstore_liquor_changelist")

            except Exception as e:
                messages.error(request, f"Error reading file: {e}")
                return redirect("admin:liquor_upload_excel")

        return render(request, "admin/liquor_upload.html")


# ======================================================
#             BAR CATEGORY + ITEMS
# ======================================================

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


# ======================================================
#                 GALLERY IMAGES
# ======================================================

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")


# ======================================================
#             EVENT + EVENT MEDIA INLINES
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
    inlines = [EventImageInline, EventVideoInline]
