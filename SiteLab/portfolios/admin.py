from django.contrib import admin
from .models import Portfolio, PortfolioTemplate, ContactMessage

@admin.register(PortfolioTemplate)
class PortfolioTemplateAdmin(admin.ModelAdmin):
    list_display = ('name','slug','order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user','is_published','last_updated')
    search_fields = ('user__username','first_name','last_name')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('portfolio','name','email','created_at','responded')
    list_filter = ('responded','created_at')
