from django.shortcuts import render

# --- MOCK DATA FOR PORTFOLIOS APP ---

MOCK_REVIEWS = [
    {'username': 'Sarah Jenkins', 'text': 'SiteLab completely transformed my portfolio. I got three job offers within a week of launching!', 'rating': 5, 'initial': 'S'},
    {'username': 'Mark D.', 'text': 'The custom website team is top-tier. They handled our complex requirements with ease.', 'rating': 5, 'initial': 'M'},
    {'username': 'Alex T.', 'text': 'Clean, modern, and super easy to use. I love the new dashboard features.', 'rating': 4.5, 'initial': 'A'},
    {'username': 'Jordan P.', 'text': 'The speed of deployment is incredible. Highly recommend for fast, professional sites.', 'rating': 5, 'initial': 'J'},
    {'username': 'Lena R.', 'text': 'Excellent value for money. The templates are high quality and easy to customize.', 'rating': 4, 'initial': 'L'},
    {'username': 'Chris B.', 'text': 'Needed a professional site fast, and SiteLab delivered. Fantastic support staff!', 'rating': 5, 'initial': 'C'},
]

MOCK_TEMPLATES = [
    {'id': 1, 'name': 'Architect Minimal', 'description': 'A clean, typography-focused design perfect for designers and writers.', 'preview_url': '/portfolios/portfolio-preview-1.html', 'color': 'text-primary', 'icon': 'fa-solid fa-pen-nib'},
    {'id': 2, 'name': 'Vibrant Developer', 'description': 'A bold, modern layout optimized for technical portfolios and code showcases.', 'preview_url': '/portfolios/portfolio-preview-2.html', 'color': 'text-warning', 'icon': 'fa-solid fa-code'},
    {'id': 3, 'name': 'Photographer Grid', 'description': 'Image-first, responsive grid layout for visual artists and photographers.', 'preview_url': '/portfolios/portfolio-preview-2.html', 'color': 'text-success', 'icon': 'fa-solid fa-camera-retro'},
    {'id': 4, 'name': 'E-Commerce Starter', 'description': 'Simple product showcase template with integrated contact and ordering sections.', 'preview_url': '/portfolios/portfolio-preview-1.html', 'color': 'text-info', 'icon': 'fa-solid fa-shopping-bag'},
]

# --- VIEW FUNCTIONS ---

def our_services(request):
    """Displays the main services overview page."""
    context = {
        'all_reviews': MOCK_REVIEWS
    }
    return render(request, 'portfolios/our-services.html', context)

def portfolio_add(request):
    """Displays the template selection page."""
    context = {
        'templates': MOCK_TEMPLATES
    }
    return render(request, 'portfolios/portfolio-add.html', context)

# Placeholder views for pages that will be created later
def portfolio_edit(request):
    return render(request, 'portfolios/portfolio-edit.html')

# def portfolio_preview_1(request):
#     return render(request, 'portfolios/portfolio-preview-1.html')

# def portfolio_preview_2(request):
#     return render(request, 'portfolios/portfolio-preview-2.html')

def portfolio_published(request):
    return render(request, 'portfolios/portfolio-published.html')

def custom_website(request):
    return render(request, 'portfolios/custom-website.html')

def add_review(request):
    return render(request, 'portfolios/add-review.html')



def get_template_data():
    """Returns mock data for template listings."""
    return [
        # Template 1: Modern Designer (Uses portfolio-preview-1.html)
        {'id': 1, 'name': 'Modern Designer', 'description': 'Clean, professional design for UI/UX and product designers.', 'icon': 'fa-solid fa-laptop-code', 'color': 'text-info', 'preview_url': '/portfolios/preview-1/'},
        
        # Template 2: Minimal Consultant (Uses portfolio-preview-2.html)
        {'id': 2, 'name': 'Minimal Consultant', 'description': 'A focused, text-heavy layout perfect for writers and consultants.', 'icon': 'fa-solid fa-user-tie', 'color': 'text-success', 'preview_url': '/portfolios/preview-2/'},
        
        # Template 3: Creative Photographer (Uses portfolio-preview-1.html)
        {'id': 3, 'name': 'Creative Photographer', 'description': 'Gallery-focused template for visual artists and photographers. Shares layout 1.', 'icon': 'fa-solid fa-camera', 'color': 'text-danger', 'preview_url': '/portfolios/preview-1/'},
        
        # Template 4: Developer Terminal (Uses portfolio-preview-2.html)
        {'id': 4, 'name': 'Developer Terminal', 'description': 'A dark-mode, code-centric theme for software engineers. Shares layout 2.', 'icon': 'fa-solid fa-terminal', 'color': 'text-secondary', 'preview_url': '/portfolios/preview-2/'},
    ]


def portfolio_preview_1(request):
    """Template Preview 1: Modern Designer / Creative Photographer layout."""
    return render(request, 'portfolios/portfolio-preview-1.html', {'template_name': 'Modern Designer'})

def portfolio_preview_2(request):
    """Template Preview 2: Minimal Consultant / Developer Terminal layout."""
    return render(request, 'portfolios/portfolio-preview-2.html', {'template_name': 'Minimal Consultant'})

