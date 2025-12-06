from django.db import models
from django.conf import settings
from django.utils import timezone
from django import template

User = settings.AUTH_USER_MODEL


register = template.Library()

@register.filter
def field_or_template(portfolio, field_name):
    return portfolio.get_field_or_template(field_name)

class PortfolioTemplate(models.Model):
    """
    Template definitions (choose one).
    Store some default values that a portfolio can fall back to.
    """
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True, help_text="FontAwesome / Bootstrap icon class")
    description = models.TextField(blank=True)
    # defaults used when a user leaves fields empty
    default_tagline = models.CharField(max_length=150, blank=True)
    default_about = models.TextField(blank=True)
    default_email = models.EmailField(blank=True)
    default_instagram = models.CharField(max_length=200, blank=True)
    default_twitter = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    template_path = models.CharField(max_length=200, default="portfolios/templates_pack/arch_minimal.html")
    preview_partial = models.CharField(max_length=255, default="")


    class Meta:
        ordering = ("order", "name")

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    template = models.ForeignKey(PortfolioTemplate, null=True, blank=True, on_delete=models.SET_NULL)

    # basic profile fields
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    tagline = models.CharField(max_length=160, blank=True)
    about = models.TextField(blank=True)

    # contact/social fields
    contact_email = models.EmailField(blank=True)
    instagram = models.CharField(max_length=200, blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)

    # projects (simple fixed fields; can be refactored to a Project model)
    project1_title = models.CharField(max_length=120, blank=True)
    project1_description = models.TextField(blank=True)
    project1_url = models.URLField(blank=True)

    project2_title = models.CharField(max_length=120, blank=True)
    project2_description = models.TextField(blank=True)
    project2_url = models.URLField(blank=True)

    project3_title = models.CharField(max_length=120, blank=True)
    project3_description = models.TextField(blank=True)
    project3_url = models.URLField(blank=True)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} portfolio"

    def display_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return getattr(self.user, 'get_full_name', lambda: self.user.username)()

    # methods to get fallback from template
    def get_field_or_template(self, field_name):
        val = getattr(self, field_name, "")
        if val:
            return val
        if self.template:
            template_field = f"default_{field_name}" if field_name in ['about','tagline','contact_email','instagram','twitter'] else None
            if template_field and hasattr(self.template, template_field):
                return getattr(self.template, template_field)
        return ""

class ContactMessage(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='messages')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} to {self.portfolio.user.username}"
