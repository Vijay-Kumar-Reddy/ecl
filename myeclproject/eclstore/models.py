from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Banner(models.Model):

    SECTION_CHOICES = [
        ('', '— No Link —'),
        ('/', 'Home'),
        ('/cigars/', 'Cigar Collection'),
        ('/bar/', 'Bar & Cocktails'),
        ('/liquor/', 'Liquor Collection'),
        ('/event_page/', 'Events'),
        ('/contact/', 'Contact'),
        ('/about/', 'About Us'),
        ('#offerings', 'Home - Offerings Section'),
        ('#gallery', 'Home - Gallery Section'),
    ]

    image = models.ImageField(upload_to="banners/", blank=True, null=True)
    video = models.FileField(upload_to="banners/videos/", blank=True, null=True)
    
    badge = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=150,blank=True, null=True)
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    tagline = models.CharField(max_length=250, blank=True, null=True)
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.CharField(
        max_length=100,
        choices=SECTION_CHOICES,
        blank=True,
        default='',
        help_text="Select which section this banner should link to."
    )
    order = models.PositiveIntegerField(default=0, help_text="Order of display on homepage")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def clean(self):
        # Enforce only 1 input allowed
        if self.image and self.video:
            raise ValidationError("Please upload either an IMAGE or a VIDEO — not both.")

        if not self.image and not self.video:
            raise ValidationError("Please upload at least one: IMAGE or VIDEO.")
        
    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"

        



class Cigar(models.Model):
    name = models.CharField(max_length=200)
    origin = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this cigar")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class CigarOffer(models.Model):
    title = models.CharField(max_length=200, help_text="Name or title of the offer")
    cigars = models.ManyToManyField(Cigar, related_name='offer_list', blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                           help_text="Discount percentage (e.g., 10 for 10%)")
    apply_to_all = models.BooleanField(default=False, help_text="If true, this offer applies to all cigars")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

    def clean(self):
        """Validation to prevent applying discounts to cigars with no price"""
        if self.discount_percent > 0:
            # Check which cigars are affected by the offer
            cigars_to_check = Cigar.objects.filter(is_active=True)
            if not self.apply_to_all:
                cigars_to_check = self.cigars.filter(is_active=True)

            # Find cigars with missing prices
            cigars_without_price = cigars_to_check.filter(price__isnull=True)

            if cigars_without_price.exists():
                cigar_names = ", ".join([c.name for c in cigars_without_price])
                raise ValidationError(
                    f"The following cigars do not have a price set and cannot receive a discount: {cigar_names}"
                )

    def get_discounted_price(self, cigar):
        """Safely calculate discounted price only if cigar has a price."""
        if cigar.price:
            return round(cigar.price - (cigar.price * (self.discount_percent / 100)), 2)
        return None




class Drink(models.Model):
    CATEGORY_CHOICES = [
        ('bar', 'Bar'),
        ('cocktail', 'Cocktail'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='bar')
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    class Meta:
        ordering = ['category', 'order']


from django.db import models

class Drink(models.Model):
    CATEGORY_CHOICES = [
        ('bar', 'Bar'),
        ('cocktail', 'Cocktail'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Controls the display order in the list.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Drink"
        verbose_name_plural = "Drinks"

    def __str__(self):
        return f"{self.name} ({self.category})"


class Liquor(models.Model):
    CATEGORY_CHOICES = [
        ('whiskey', 'Whiskey'),
        ('rum', 'Rum'),
        ('vodka', 'Vodka'),
        ('gin', 'Gin'),
        ('tequila', 'Tequila'),
        ('wine', 'Wine'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Liquor"
        verbose_name_plural = "Liquors"

    def __str__(self):
        return f"{self.name} ({self.category})"
    
    


class BarCategory(models.Model):
    """Category for grouping bar menu items."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Bar Categories"

    def __str__(self):
        return self.name


class BarItem(models.Model):
    """Individual item in the bar menu."""
    category = models.ForeignKey(
        BarCategory, on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name





class Event(models.Model):
    """Dynamic event model for upcoming and past events."""
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField()
    time = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Controls display order manually if needed.")

    class Meta:
        ordering = ['order', '-date']

    def __str__(self):
        return f"{self.title} ({self.date})"

    def is_upcoming(self):
        """True if event date is in the future."""
        return self.date >= timezone.now().date()


class GalleryImage(models.Model):
    image = models.ImageField(upload_to="gallery/")
    title = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or "Gallery Image"


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="event_gallery/images/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Image for {self.event.title}"


class EventVideo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="event_gallery/videos/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Video for {self.event.title}"
