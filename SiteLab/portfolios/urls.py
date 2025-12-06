from django.urls import path
from . import views

app_name = 'portfolios'

urlpatterns = [
    path('choose-template/', views.choose_template_view, name='choose_template_view'),
    path('edit/', views.edit_portfolio_view, name='edit_portfolio_view'),
    path('preview/', views.preview_view, name='preview_view'),
    path("preview-template/", views.template_preview_view, name="template_preview_view"),
    path('publish/', views.publish_portfolio, name='publish_portfolio'),
    path('u/<str:username>/', views.published_view, name='published_view'),
    path('u/<str:username>/contact/', views.submit_contact_view, name='submit_contact_view'),
]
