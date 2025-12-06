from django.core.management.base import BaseCommand
from portfolios.models import PortfolioTemplate

class Command(BaseCommand):
    help = "Load portfolio templates"

    def handle(self, *args, **kwargs):

        TEMPLATES = [
            {
                "slug": "arch-minimal",
                "name": "Architect Minimal",
                "description": "Clean layout with strong typography",
                "icon_class": "fa-solid fa-pen-nib",
                "template_path": "portfolios/templates_pack/arch_minimal.html",
                "preview_partial": "portfolios/templates_pack/arch_minimal_preview.html"
            },
            {
                "slug": "pro-designer",
                "name": "Professional Designer",
                "description": "Modern layout for creative designers",
                "icon_class": "fa-solid fa-palette",
                "template_path": "portfolios/templates_pack/pro_designer.html",
                "preview_partial": "portfolios/templates_pack/pro_designer_preview.html",
            },
            {
                "slug": "creative-photographer",
                "name": "Creative Photographer",
                "description": "Full-image template for photographers",
                "icon_class": "fa-solid fa-camera",
                "template_path": "portfolios/templates_pack/creative_photographer.html",
                "preview_partial": "portfolios/templates_pack/creative_photographer_preview.html",
                
            },
            {
                "slug": "dev-terminal",
                "name": "Developer Terminal",
                "description": "Dark theme like a real terminal",
                "icon_class": "fa-solid fa-terminal",
                "template_path": "portfolios/templates_pack/dev_terminal.html",
                "preview_partial": "portfolios/templates_pack/dev_terminal_preview.html",
            },
        ]

        for data in TEMPLATES:
            PortfolioTemplate.objects.update_or_create(
                slug=data["slug"],
                defaults=data
            )

        self.stdout.write(self.style.SUCCESS("Portfolio templates loaded successfully."))
