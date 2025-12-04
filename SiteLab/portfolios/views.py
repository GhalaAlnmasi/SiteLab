from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms.models import model_to_dict
from .models import Portfolio, PortfolioTemplate
from .forms import PortfolioForm
from django.contrib.auth import get_user_model
from django.db import IntegrityError 


MOCK_REVIEWS = [
    {'username': 'Sarah Jenkins', 'text': 'SiteLab completely transformed my portfolio. I got three job offers within a week of launching!', 'rating': 5, 'initial': 'S'},
    {'username': 'Mark D.', 'text': 'The custom website team is top-tier. They handled our complex requirements with ease.', 'rating': 5, 'initial': 'M'},
    {'username': 'Alex T.', 'text': 'Clean, modern, and super easy to use. I love the new dashboard features.', 'rating': 4.5, 'initial': 'A'},
    {'username': 'Jordan P.', 'text': 'The speed of deployment is incredible. Highly recommend for fast, professional sites.', 'rating': 5, 'initial': 'J'},
    {'username': 'Lena R.', 'text': 'Excellent value for money. The templates are high quality and easy to customize.', 'rating': 4, 'initial': 'L'},
    {'username': 'Chris B.', 'text': 'Needed a professional site fast, and SiteLab delivered. Fantastic support staff!', 'rating': 5, 'initial': 'C'},
]

def portfolio_add(request):
    templates = PortfolioTemplate.objects.all()
    return render(request, 'portfolios/portfolio-add.html', {'templates': templates})


def _get_portfolio_instance(user_pk, selected_template_id=1):
    """Fetches or creates the portfolio instance for the mock user."""
    try:
        portfolio = Portfolio.objects.get(pk=user_pk)
        
        if portfolio.template_id != selected_template_id:
             portfolio.template_id = selected_template_id
             portfolio.save() 
        
    except Portfolio.DoesNotExist:
        try:
            User = get_user_model()
            mock_user = User.objects.get(pk=user_pk)
            
            portfolio = Portfolio(
                user=mock_user, 
                template_id=selected_template_id
            )
            
        except User.DoesNotExist:
             print(f"CRITICAL ERROR: Mock User with PK={user_pk} does not exist. Cannot create Portfolio.")
             portfolio = Portfolio(template_id=selected_template_id)
             
    except Exception as e:
        print(f"An unexpected error occurred during portfolio retrieval/creation: {e}")
        portfolio = Portfolio(template_id=selected_template_id)
        
    return portfolio


@login_required
def portfolio_edit(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    selected_template_id = request.GET.get('template')
    if selected_template_id:
        try:
            portfolio.template = PortfolioTemplate.objects.get(pk=selected_template_id)
            portfolio.save()
        except PortfolioTemplate.DoesNotExist:
            pass

    if request.method == "POST":
        form = PortfolioForm(request.POST, instance=portfolio)

        if form.is_valid():
            portfolio = form.save(commit=False)

            if 'publish' in request.POST:
                portfolio.is_published = True

            portfolio.save()

            return redirect("portfolios:portfolio_edit")

    else:
        form = PortfolioForm(instance=portfolio)

    return render(request, "portfolios/portfolio-edit.html", {
        "form": form,
        "current_template": portfolio.template,
        "templates": PortfolioTemplate.objects.all(),
    })

def portfolio_published(request):
    portfolio_instance, portfolio_data = _get_portfolio_data()
    
    if not portfolio_instance.is_published:
        return redirect(f"{redirect('portfolios:portfolio_edit').url}?template_id={portfolio_instance.template_id}")
        
    live_url = request.build_absolute_uri(redirect('portfolios:published_view').url)
    
    return render(request, 'portfolios/portfolio-published.html', {'live_url': live_url})


def _get_portfolio_data(user_id=MOCK_USER_PK):
    """Helper to fetch or create portfolio data for rendering."""
    try:
        portfolio = Portfolio.objects.get(pk=user_id)
        return portfolio, model_to_dict(portfolio)
    except Portfolio.DoesNotExist:
        portfolio = Portfolio() 
        portfolio.template_id = 1
        return portfolio, model_to_dict(portfolio)

@login_required
def preview_view(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)

    return render(request, 'portfolios/preview.html', {
        "portfolio": portfolio,
        "template_path": portfolio.get_template_path(),
        "template": portfolio.template
    })

def published_view(request, username):
    user = get_object_or_404(User, username=username)
    portfolio = get_object_or_404(Portfolio, user=user)

    if not portfolio.is_published:
        return redirect("portfolios:portfolio_edit")

    return render(request, 'portfolios/published.html', {
        "portfolio": portfolio,
        "template_path": portfolio.get_template_path(),
        "template": portfolio.template
    })

def template1_view(request):
    return render(request, 'portfolios/portfolio_template1.html')

def template2_view(request):
    return render(request, 'portfolios/portfolio_template2.html')

def template3_view(request):
    return render(request, 'portfolios/portfolio_template3.html')

def template4_view(request):
    return render(request, 'portfolios/portfolio_template4.html')