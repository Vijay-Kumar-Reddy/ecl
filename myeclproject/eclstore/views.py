from django.shortcuts import render
from django.utils import timezone
from .models import *
from django.contrib import messages
from django.shortcuts import redirect

def index(request):
    
    banners = Banner.objects.filter(is_active=True).order_by('order')
    
    #Offerings section
    
    offerings = [
        {
            "name": "Premium Cigar Lounge",
            "category": "Cigar",
            "description": "Exclusive single malts and limited editions from around the world.",
            "image": "static/images/cigar_lounge.png",
        },
        {
            "name": "Luxury Bar & Cocktails",
            "category": "bar",
            "description": "Timeless recipes crafted with premium ingredients.",
            "image": "static/images/bar.png",
        },
        {
            "name": "Premium Liquor Collection",
            "category": "liquor",
            "description": "Authentic Havana cigars stored in perfect conditions.",
            "image": "static/images/liquor.png",
        },
    ]
    
    #--------------------------------------
    
    #Gallery section
    gallery_images = [
        {
            "url": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800",
            "alt": "Luxury Bar Interior"
        },
        {
            "url": "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=800",
            "alt": "Whiskey Bottle Close-up"
        },
        {
            "url": "https://images.unsplash.com/photo-1606312619070-d48b4c652a52?w=800",
            "alt": "Cigar Lounge"
        },
        {
            "url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800",
            "alt": "Cigars Display"
        },
        {
            "url": "https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=800",
            "alt": "Champagne Glasses"
        },
        {
            "url": "https://images.unsplash.com/photo-1569529465841-dfecdab7503b?w=800",
            "alt": "Premium Liquor Collection"
        },
    ]
    
    return render(request, "base.html", {
        "banners": banners,
        "slide_duration": 10000,  # milliseconds
        "offerings": offerings,
        "gallery_images": gallery_images,
    })




def cigar_collection(request):
    cigars = Cigar.objects.filter(is_active=True).order_by('order')
    offers = CigarOffer.objects.filter(is_active=True).order_by('order')
    hero_image = "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=1920"
    
    offer_data = []

    for offer in offers:
        applicable_cigars = cigars if offer.apply_to_all else offer.cigars.filter(is_active=True)
        cigar_data = []

        for cigar in applicable_cigars:
            offer_price = offer.get_discounted_price(cigar)
            cigar_data.append({
                'name': cigar.name,
                'old_price': cigar.price if cigar.price else "—",
                'offer_price': offer_price if offer_price else "—",
            })

        # Only include if there’s at least one cigar
        if cigar_data:
            offer_data.append({
                'offer': offer,
                'cigars': cigar_data
            })
        
    context = {
        'hero_image': hero_image,
        'cigars': cigars,
        'offers': offer_data,  # ✅ Use structured offer data
    }

    return render(request, 'offerings/cigars.html', context)


# Bar and Cocktail View
# ------------------------------------------
def bar_and_cocktail(request):
    # Background image (stored in /static/images/)
    hero_image = "images/bar.png"

    # Separate drinks by category
    drinks = Drink.objects.filter(category="bar", is_active=True).order_by("order")
    cocktails = Drink.objects.filter(category="cocktail", is_active=True).order_by("order")

    context = {
        "hero_image": hero_image,
        "drinks": drinks,
        "cocktails": cocktails,
    }
    return render(request, "offerings/bar.html", context)



def liquor_collection(request):
    hero_image = "images/liquor.png"  # static/images/liquor_hero.jpg

    # Get liquors grouped by category
    collections = {}
    liquors = Liquor.objects.filter(is_active=True).order_by('order', 'name')

    for liquor in liquors:
        collections.setdefault(liquor.get_category_display(), []).append(liquor)

    context = {
        "hero_image": hero_image,
        "collections": collections,
    }
    return render(request, "offerings/liquor.html", context)


def bar_menu(request):
    hero_image = "images/bar_hero.jpg"
    categories = BarCategory.objects.filter(is_active=True).prefetch_related("items").order_by("order")

    # Split categories evenly into two columns
    category_list = list(categories)
    mid = len(category_list) // 2
    left_categories = category_list[:mid]
    right_categories = category_list[mid:]

    return render(request, "offerings/bar_menu.html", {
        "hero_image": hero_image,
        "left_categories": left_categories,
        "right_categories": right_categories,
    })



def event_page(request):
    # Hero banner (static image)
    hero_image = "images/event-nov.png"

    # Fetch events dynamically
    events = Event.objects.filter(is_active=True)
    upcoming_events = [e for e in events if e.is_upcoming()]
    past_events = [e for e in events if not e.is_upcoming()]

    context = {
        "hero_image": hero_image,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
    }
    return render(request, "events/event_page.html", context)




#banner section
    # banners = [
    #     {
    #         "image": "/static/images/hero_banner.png",
    #         "badge": "Premium Lounge",
    #         "title": "Welcome to Eiland Cigar Lounge",
    #         "subtitle": "Experience luxury, leisure, and lifestyle.",
    #         "tagline": "Exclusive cigars • Fine spirits • Timeless moments",
    #         "button_text": "Explore Now",
    #         "button_link": "#",
    #     },
    #     {
    #         "image": "/static/images/event-nov.png",
    #         "badge": "Don't Miss : November 22nd 2025",
    #         "title": "The Grand Reserve: A Night of Smoke, Spirits, and Soul",
    #         "subtitle": "Featuring Master Cigar Rollers, Premier Brands, and Gourmet Food Trucks",
    #         "tagline": "Smoke •Sip •Savor",
    #         "button_text": "Visit Us",
    #         "button_link": "#",
    #     },
    #     {
    #         "image": "/static/images/hero-bg.png",
    #         "badge": "Refined Taste",
    #         "title": "Premium Cigars & Ambience",
    #         "subtitle": "Where class meets comfort.",
    #         "tagline": "The finest blends in a luxurious setting",
    #         "button_text": "Visit Us",
    #         "button_link": "#",
    #     },
    #     {
    #         "image": "/static/images/home_page.png",
    #         "badge": "Luxury Experience",
    #         "title": "Unwind in Style",
    #         "subtitle": "The perfect spot for every occasion.",
    #         "tagline": "Sip • Smoke • Socialize",
    #         "button_text": "Book a Table",
    #         "button_link": "#",
    #     },

    # ]
    
    #--------------------------------------
    
    
    
      # cigars = [
    #     {'name': 'Cohiba Robusto', 'price': 45.00},
    #     {'name': 'Montecristo No.2', 'price': 38.50},
    #     {'name': 'Arturo Fuente Hemingway', 'price': 29.00},
    #     {'name': 'Davidoff Grand Cru', 'price': 42.00},
    #     {'name': 'Romeo y Julieta Short Churchill', 'price': 36.00},
    #     {'name': 'Padron 1964 Anniversary Maduro', 'price': 52.00},
    # ]

    # offers = [
    #     {'name': 'Cohiba Robusto', 'old_price': 45.00, 'offer_price': 39.00},
    #     {'name': 'Arturo Fuente Hemingway', 'old_price': 29.00, 'offer_price': 24.50},
    #     {'name': 'Davidoff Grand Cru', 'old_price': 42.00, 'offer_price': 37.00},
    # ]
    
    

# def bar_and_cocktail(request):
#     drinks = [
#         {'name': 'Johnnie Walker Blue Label', 'price': 45},
#         {'name': 'Macallan 18 Years', 'price': 65},
#         {'name': 'Jack Daniels Single Barrel', 'price': 40},
#     ]

#     cocktails = [
#         {'name': 'Old Fashioned', 'price': 22},
#         {'name': 'Mojito', 'price': 18},
#         {'name': 'Whiskey Sour', 'price': 20},
#     ]

#     return render(request, 'offerings/bar.html', {
#         'hero_image': 'images/bar.png',  # from static/images/
#         'drinks': drinks,
#         'cocktails': cocktails,
#     })

#---------------------------------------------


# Liquor Collection View
#---------------------------------------------
# def liquor_collection(request):
#     collections = {
#         "Whiskey": [
#             {"name": "Macallan 18 Years", "price": 65},
#             {"name": "Glenfiddich 15", "price": 58},
#             {"name": "Johnnie Walker Blue Label", "price": 45},
#         ],
#         "Rum": [
#             {"name": "Mount Gay XO", "price": 38},
#             {"name": "Diplomatico Reserva", "price": 42},
#         ],
#         "Vodka": [
#             {"name": "Grey Goose", "price": 35},
#             {"name": "Belvedere", "price": 37},
#         ],
#         "Tequila": [
#             {"name": "Don Julio 1942", "price": 70},
#             {"name": "Patrón Silver", "price": 55},
#         ],
#         "Wine": [
#             {"name": "Château Margaux", "price": 90},
#             {"name": "Robert Mondavi Cabernet Sauvignon", "price": 60},
#         ],
#     }
#     return render(request, "offerings/liquor.html", {
#         "hero_image": "images/liquor.png",  # static/images/liquor_hero.jpg
#         "collections": collections,
#     })