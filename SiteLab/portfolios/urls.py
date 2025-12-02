from django.urls import path
from . import views

# Define the app namespace for use in {% url 'portfolios:view_name' %}
app_name = 'portfolios'

urlpatterns = [
    path('our-services/', views.our_services, name='our_services'),
    path('portfolio-add/', views.portfolio_add, name='portfolio_add'),
    path('portfolio-edit/', views.portfolio_edit, name='portfolio_edit'),
    path('portfolios/portfolio-preview-1/', views.portfolio_preview_1, name='portfolio_preview_1'),
    path('portfolios/portfolio-preview-2/', views.portfolio_preview_2, name='portfolio_preview_2'),
    path('portfolio-published/', views.portfolio_published, name='portfolio_published'),
    path('custom-website/', views.custom_website, name='custom_website'),
    path('add-review/', views.add_review, name='add_review'),
]