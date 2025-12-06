from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.http import  HttpResponse, Http404, HttpResponseForbidden
from .models import Portfolio, PortfolioTemplate, ContactMessage
from .forms import PortfolioForm, ContactForm

def published_view(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)

    portfolio = get_object_or_404(Portfolio, user=user)

    # allow preview mode even if not published
    preview_mode = request.GET.get("preview") == "1"

    if not portfolio.is_published and not preview_mode:
        return HttpResponseForbidden("Portfolio not public")

    template_path = portfolio.template.template_path

    return render(request, template_path, {
        'portfolio': portfolio,
        'contact_form': ContactForm(),
        'preview_mode': preview_mode,
    })


@login_required
def preview_view(request):
    portfolio = getattr(request.user, "portfolio", None)
    if not portfolio:
        return redirect('portfolios:edit_portfolio_view')

    return render(request, "portfolios/portfolio_preview.html", {
        "portfolio": portfolio,
        "preview_mode": True,
    })


@login_required
def template_preview_view(request):
    portfolio = getattr(request.user, "portfolio", None)

    if not portfolio:
        return HttpResponse("No portfolio.", status=404)

    return render(request, "portfolios/preview_base.html", {
        "portfolio": portfolio,
        "contact_form": ContactForm(),
        "preview_mode": True,
    })



@login_required
def choose_template_view(request):
    templates = PortfolioTemplate.objects.all()
    if request.method == "POST":
        slug = request.POST.get('template_slug')
        tmpl = get_object_or_404(PortfolioTemplate, slug=slug)
        portfolio = getattr(request.user, 'portfolio', None)
        if not portfolio:
            portfolio = Portfolio.objects.create(user=request.user, template=tmpl)
        else:
            portfolio.template = tmpl
            portfolio.save()
        messages.success(request, "Template selected. Now you can edit your portfolio.")
        return redirect('portfolios:edit_portfolio_view')
    return render(request, 'portfolios/choose_template.html', {'templates': templates})

@login_required
def edit_portfolio_view(request):
    portfolio = getattr(request.user, 'portfolio', None)
    if not portfolio:
        portfolio = Portfolio.objects.create(user=request.user)

    back_url = request.GET.get('next') or reverse('portfolios:edit_portfolio_view')

    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)

        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if form.is_valid():
            try:
                with transaction.atomic():
                    p = form.save(commit=False)
                    p.user = request.user
                    p.save()

                if is_ajax:
                    return HttpResponse(status=200)

                if 'save_and_view' in request.POST:
                    return redirect('portfolios:preview_view')

                messages.success(request, "Portfolio saved successfully.")
                return redirect(back_url)

            except Exception as e:
                if is_ajax:
                    return HttpResponse(status=500)
                messages.error(request, "Error saving portfolio. Please try again.")
        else:
            if is_ajax:
                return HttpResponse(status=400)
            messages.error(request, "Please fix the errors below.")

    else:
        form = PortfolioForm(instance=portfolio)

    templates = PortfolioTemplate.objects.all()
    return render(request, 'portfolios/edit_portfolio.html', {
        'form': form,
        'portfolio': portfolio,
        'templates': templates,
        'back_url': back_url
    })


@login_required
def publish_portfolio(request):
    portfolio = getattr(request.user, 'portfolio', None)
    if not portfolio:
        messages.error(request, "No portfolio to publish.")
        return redirect('portfolios:edit_portfolio_view')

    live_url = request.build_absolute_uri(
        reverse('portfolios:published_view', args=[request.user.username])
    )

    if portfolio.is_published:
        return render(request, "portfolios/already_published.html", {
            "live_url": live_url
        })

    portfolio.is_published = True
    portfolio.save()

    return render(request, "portfolios/publish_success.html", {
        "live_url": live_url
    })

def submit_contact_view(request, username):
    """
    Visitors submit a contact message from published portfolio.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    try:
        portfolio = user.portfolio
    except Portfolio.DoesNotExist:
        raise Http404
    if not portfolio.is_published:
        return HttpResponseForbidden("Portfolio not public")

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.portfolio = portfolio
            msg.save()
            # Optionally: send email to portfolio.contact_email
            messages.success(request, "Message sent. The user will contact you soon (if they check).")
            return redirect(reverse('portfolios:published_view', args=[username]))
        else:
            messages.error(request, "Please correct the errors in the contact form.")
            return redirect(reverse('portfolios:published_view', args=[username]))
    return redirect(reverse('portfolios:published_view', args=[username]))
