from django.db import models
from django.contrib.auth import get_user_model
# from django.db.models import JSONField

User = get_user_model()

class PortfolioTemplate(models.Model):
    """
    Template definitions (shared across users).
    Only contains metadata and the template_path to include.
    """
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="FontAwesome class, e.g., 'fa-solid fa-camera'")
    description = models.TextField(default="", blank=True)

    default_first_name = models.CharField(max_length=50, default="Samantha") 
    default_last_name = models.CharField(max_length=50, default="Doe")  
    default_tagline = models.CharField(max_length=255, default="Senior UX/UI Designer & Web Developer")
    default_about_me = models.TextField(default="A seasoned professional dedicated to crafting visually stunning and highly functional digital experiences.")
    default_contact_email = models.EmailField(default="contact@samanthajdoe.com")

    template_path = models.CharField(
        max_length=255,
        default="portfolios/portfolio_template1.html",
        help_text="Path to the HTML template (use Django include)"
    )

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    """
    Per-user portfolio content. This stores the actual editable fields that will be
    used by the preview and published pages. Each user has one Portfolio.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="portfolio"
    )

    template = models.ForeignKey(
        PortfolioTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portfolios"
    )

    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="First Name")
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Last Name")
   
    tagline = models.CharField(max_length=255, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    # Project 1
    project1_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Project 1 Title")
    project1_description = models.TextField(blank=True, null=True, verbose_name="Project 1 Description")
    project1_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Project 1 URL")

    # Project 2
    project2_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Project 2 Title")
    project2_description = models.TextField(blank=True, null=True, verbose_name="Project 2 Description")
    project2_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Project 2 URL")

    # Project 3
    project3_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Project 3 Title")
    project3_description = models.TextField(blank=True, null=True, verbose_name="Project 3 Description")
    project3_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Project 3 URL")
 

    is_published = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio of {self.user.username}"

    def get_template_path(self):
        """
        Returns the template path based on the template object.
        """
        return self.template.template_path if self.template else "portfolios/default.html"
    
    def get_projects_list(self):
        """
        Reconstructs the list of projects from the individual fields for template context.
        """
        projects = []
        for i in range(1, 4):
            title = getattr(self, f'project{i}_title')
            description = getattr(self, f'project{i}_description')
            url = getattr(self, f'project{i}_url')

            if title:
                projects.append({
                    'title': title,
                    'description': description or "",
                    'url': url or "#",             
                })
        return projects

    def get_field_or_default(self, field_name):
        """
        Helper to return the portfolio field if set, otherwise return the template default.
        This can be used in views if you want to build a context object that always has values.
        """
        val = getattr(self, field_name, None)
        if val:
            return val
        if self.template:
            template_default_name = f"default_{field_name}"
            return getattr(self.template, template_default_name, "")
        return ""
